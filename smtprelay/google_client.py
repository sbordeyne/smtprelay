from base64 import urlsafe_b64encode
from email.message import EmailMessage
import json
import logging

from aiosmtpd.smtp import Envelope
from kubernetes import client
from kubernetes.config import load_incluster_config
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google_auth_oauthlib.helpers import session_from_client_config, credentials_from_session

from smtprelay import config
from smtprelay.client_interface import ClientInterface


logger = logging.getLogger("smtprelay.google_client")


class GoogleClient(ClientInterface):
    SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

    def _get_client(self):
        creds = None
        load_incluster_config()
        v1 = client.CoreV1Api()
        # try to read existing creds from the cluster
        secrets = v1.list_namespaced_secret(
            config.KUBE_NAMESPACE,
            label_selector="app.kubernetes.io/name=smtp-relay",
        )
        secret_names = [secret.metadata.name for secret in secrets.items]
        if "smtp-relay-google-creds" in secret_names:
            secret = v1.read_namespaced_secret("smtp-relay-google-creds", config.KUBE_NAMESPACE)
            session, client_config = session_from_client_config(
                (json.loads(secret.data["credentials.json"])),
                scopes=self.SCOPES,
            )
            creds = credentials_from_session(session, client_config)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                logger.info("Refreshing expired credentials")
                creds.refresh(Request())
            else:
                logger.info("No credentials found, asking for new ones")
                flow = InstalledAppFlow.from_client_secrets_file(
                    config.SMTP_GMAIL_CREDENTIALS_PATH, self.SCOPES
                )
                flow.redirect_uri = (
                    f"http://{config.SMTP_GMAIL_AUTH_REDIRECT_HOST}:{config.SMTP_GMAIL_AUTH_SERVER_PORT}/"  # noqa
                )
                url, state = flow.authorization_url()
                logger.info("Please go to %s and authorize access. state=%s", url, state)
                creds = flow.run_local_server(
                    host=config.SMTP_GMAIL_AUTH_REDIRECT_HOST,
                    bind_addr="0.0.0.0",
                    port=config.SMTP_GMAIL_AUTH_SERVER_PORT,
                    open_browser=False,
                )

            if "smtp-relay-google-creds" in secret_names:
                # Update the existing secret
                v1.patch_namespaced_secret(
                    namespace=config.KUBE_NAMESPACE,
                    name="smtp-relay-google-creds",
                    body=client.V1Secret(
                        metadata=client.V1ObjectMeta(
                            name="smtp-relay-google-creds",
                            namespace=config.KUBE_NAMESPACE,
                        ),
                        data={"credentials.json": json.dumps(creds.to_json())},
                    ),
                )
            else:
                # Save the credentials for the next run
                v1.create_namespaced_secret(
                    namespace=config.KUBE_NAMESPACE,
                    body=client.V1Secret(
                        metadata=client.V1ObjectMeta(
                            name="smtp-relay-google-creds",
                            namespace=config.KUBE_NAMESPACE,
                        ),
                        data={"credentials.json": json.dumps(creds.to_json())},
                    ),
                )
        return build("gmail", "v1", credentials=creds)

    def __enter__(self):
        self.client = self._get_client()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return

    def send_message(self, envelope: Envelope, message: EmailMessage) -> None:
        self.client.users().messages().send(
            userId="me",
            body=self._build_message(message),
        ).execute()
        return

    def _build_message(self, message: EmailMessage) -> dict[str, str]:
        return {'raw': urlsafe_b64encode(message.as_bytes()).decode()}
