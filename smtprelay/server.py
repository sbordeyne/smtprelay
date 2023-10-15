import logging
from email.message import EmailMessage
from email.parser import Parser
from typing import Mapping

from aiosmtpd.smtp import Envelope, Session, SMTP

from smtprelay import config, smtp_client, google_client, mailjet_client
from smtprelay.client_interface import ClientInterface


logger = logging.getLogger("smtprelay.server")


class SMTPHandler:
    async def handle_RCPT(
        self,
        server: SMTP,
        session: Session,
        envelope: Envelope,
        address: str,
        rcpt_options: dict,
    ):
        logger.info("Got RCPT for %s with options %s", address, rcpt_options)
        envelope.rcpt_tos.append(address)
        envelope.rcpt_options.extend(rcpt_options)
        return "250 OK"

    async def handle_MAIL(
        self,
        server: SMTP,
        session: Session,
        envelope: Envelope,
        address: str,
        mail_options: dict,
    ):
        logger.info("Got MAIL from %s with options %s", address, mail_options)
        envelope.mail_from = address
        envelope.mail_options.extend(mail_options)
        return "250 OK"

    async def handle_DATA(
        self, server: SMTP, session: Session, envelope: Envelope
    ) -> str:
        logger.info(
            "Got DATA with envelope %s, sending using %s",
            envelope,
            config.SMTP_SERVICE,
        )
        services: Mapping[str, ClientInterface] = {
            "smtp": smtp_client.SMTPClient,
            "google": google_client.GoogleClient,
            "mailjet": mailjet_client.MailjetClient,
        }
        service = services.get(config.SMTP_SERVICE.lower(), smtp_client.SMTPClient)
        logger.debug(
            "Service found for key %s: %s",
            config.SMTP_SERVICE, service.__class__.__name__,
        )
        logger.info("Parsing message from envelope")
        message = Parser(EmailMessage).parsestr(envelope.content)
        with service() as smtpd:
            smtpd.send_message(envelope, message)
        return "250 Message accepted for delivery"

    async def handle_EHLO(
        self,
        server: SMTP,
        session: Session,
        envelope: Envelope,
        hostname: str,
        responses: list[str],
    ) -> list[str]:
        logger.info("Got EHLO from %s", hostname)
        session.host_name = hostname
        return responses

    async def handle_HELO(
        self, server: SMTP, session: Session, envelope: Envelope, hostname: str
    ) -> str:
        logger.info("Got HELO from %s", hostname)
        session.host_name = hostname
        return f"250 {server.hostname}"

    async def handle_QUIT(self, server: SMTP, session: Session, envelope: Envelope):
        logger.info("Got QUIT")
        return "221 Bye"

    async def handle_NOOP(
        self, server: SMTP, session: Session,
        envelope: Envelope, arg: str,
    ) -> str:
        logger.info("Got NOOP with arg %s", arg)
        return "250 OK"

    async def handle_exception(self, error: Exception) -> str:
        logger.exception("Error while handling SMTP request: ", exc_info=error)
        return "542 Internal server error"
