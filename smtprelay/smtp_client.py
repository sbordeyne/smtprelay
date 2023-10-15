import logging
from email.message import EmailMessage
import smtplib

from aiosmtpd.smtp import Envelope

from smtprelay import config
from smtprelay.client_interface import ClientInterface


logger = logging.getLogger("smtprelay.smtp_client")


class SMTPClient(ClientInterface):
    def __enter__(self):
        logger.info(
            "Connecting to SMTP client %s:%s",
            config.SMTP_CLIENT_HOSTNAME,
            config.SMTP_CLIENT_PORT,
        )

        if config.SMTP_CLIENT_USE_SSL:
            logger.info("Using SSL client")
            self.client = smtplib.SMTP_SSL(
                config.SMTP_CLIENT_HOSTNAME, port=int(config.SMTP_CLIENT_PORT),
            )
        else:
            logger.info("Using non-SSL client")
            self.client = smtplib.SMTP(
                config.SMTP_CLIENT_HOSTNAME, port=int(config.SMTP_CLIENT_PORT),
            )
        if config.SMTP_CLIENT_USE_AUTH:
            logger.info(
                "Logging in with username %s and password %s",
                config.SMTP_CLIENT_LOGIN,
                config.SMTP_CLIENT_PASSWORD[:3] + "*" * (len(config.SMTP_CLIENT_PASSWORD) - 3),
            )
            self.client.login(config.SMTP_CLIENT_LOGIN, config.SMTP_CLIENT_PASSWORD)
        return self

    def send_message(self, envelope: Envelope, message: EmailMessage) -> None:
        logger.info(
            "Sending mail %s from %s to %s",
            envelope.content.splitlines()[0],
            envelope.mail_from,
            envelope.rcpt_tos,
        )
        try:
            return_value = self.client.sendmail(
                envelope.mail_from,
                envelope.rcpt_tos,
                envelope.content.decode("utf-8"),
                envelope.mail_options,
                envelope.rcpt_options,
            )
            logger.info("SMTP client returned: %s", return_value)
        except smtplib.SMTPException as exc:
            logger.exception(
                "SMTP Error (%s) while sending the message: ",
                exc.__class__.__name__,
                exc_info=exc,
            )
        return

    def __exit__(self, exc_type, exc_value, traceback):
        logger.info("Closing SMTP client")
        self.client.quit()
