from abc import ABCMeta, abstractmethod
from email.message import EmailMessage

from aiosmtpd.smtp import Envelope


class ClientInterface(metaclass=ABCMeta):
    @abstractmethod
    def __enter__(self):
        ...

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        ...

    @abstractmethod
    def send_message(self, envelope: Envelope, message: EmailMessage) -> None:
        ...

    def strmsg(self, message: EmailMessage) -> str:
        """Return a compact string representation of the message"""
        return f"{message['Subject']} from {message['From']} to {message['To']}"
