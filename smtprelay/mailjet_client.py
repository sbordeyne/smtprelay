from base64 import b64encode
from email.message import EmailMessage
import json
import logging
from mimetypes import guess_type
import time

from aiosmtpd.smtp import Envelope
from mailjet_rest import Client
import requests

from smtprelay import config
from smtprelay.client_interface import ClientInterface


logger = logging.getLogger("smtprelay.mailjet_client")


class MailjetClient(ClientInterface):
    def __enter__(self):
        logger.info("Connecting to Mailjet client %s", config.SMTP_MAILJET_API_VERSION)
        logger.info(
            "API Key: %s ; API Secret: %s",
            config.SMTP_MAILJET_API_KEY[:5] + "*" * (len(config.SMTP_MAILJET_API_KEY) - 5),
            config.SMTP_MAILJET_API_SECRET[:5] + "*" * (len(config.SMTP_MAILJET_API_SECRET) - 5),
        )

        self.client = Client(
            auth=(config.SMTP_MAILJET_API_KEY, config.SMTP_MAILJET_API_SECRET),
            version=config.SMTP_MAILJET_API_VERSION,
        )
        return self

    def get_attachments(self, message: EmailMessage) -> list[dict[str, str]]:
        logger.info("Getting attachments from message %s", self.strmsg(message))
        attachments = []
        for part in message.walk():
            logger.debug("Parsing part %s", part)
            if part.get_content_maintype() == 'multipart':
                logger.debug("Part %s has content maintype multipart, skipping", self.strmsg(part))
                continue
            if part.get('Content-Disposition') is None:
                logger.debug("Part %s has no Content-Disposition, skipping", self.strmsg(part))
                continue
            file_name = part.get_filename()
            if file_name:
                mimetype = guess_type(file_name)[0] or "text/plain"
                logger.debug(
                    "Part %s has file name %s: mimetype %s",
                    self.strmsg(part), file_name, mimetype,
                )
                attachments.append(
                    {
                        "Content-type": mimetype,
                        "Filename": file_name,
                        "Content": b64encode(part.get_payload(decode=True)).decode("utf-8"),
                    }
                )
        return attachments

    def send_message(self, envelope: Envelope, message: EmailMessage) -> None:
        logger.info("MailjetClient::send_message -- Building JSON payload")
        data = {
            "FromEmail": envelope.mail_from,
            "FromName": envelope.mail_from.split("@")[0],
            "Subject": message["Subject"],
            "Recipients": [{"Email": rcpt} for rcpt in envelope.rcpt_tos],
            "Attachments": self.get_attachments(message),
        }
        logger.info("MailjetClient::send_message -- Sending message %s", json.dumps(data))
        response: requests.Response = self.client.send.create(data=data)
        response.raise_for_status()
        time.sleep(5)
        logger.info(
            "MailjetClient::send_message -- Message sent, returned %s, body: %s",
            response.status_code, response.json(),
        )
        return None

    def __exit__(self, exc_type, exc_val, exc_tb):
        ...
        return None
