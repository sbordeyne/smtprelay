import os
import logging

levelmap = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "warn": logging.WARNING,
    "error": logging.ERROR,
    "exception": logging.ERROR,
}

KUBE_NAMESPACE = os.getenv("NAMESPACE", "default")

SMTP_SERVER_HOSTNAME = os.getenv("SMTP_SERVER_HOSTNAME", "smtp-relay.smtp-relay.svc.cluster.local")
SMTP_SERVER_PORT = int(os.getenv("SMTP_SERVER_PORT", "8025"))

SMTP_CLIENT_HOSTNAME = os.getenv("SMTP_CLIENT_HOSTNAME")
SMTP_CLIENT_PORT = int(os.getenv("SMTP_CLIENT_PORT", "25"))
SMTP_CLIENT_USE_SSL = os.getenv("SMTP_CLIENT_USE_SSL", "false").lower() in ("true", "yes", "1", "y")
SMTP_CLIENT_USE_AUTH = os.getenv("SMTP_CLIENT_USE_AUTH", "").lower() in ("true", "yes", "1", "y")
SMTP_CLIENT_LOGIN = os.getenv("SMTP_CLIENT_LOGIN", "simon.bordeyne@gmail.com")
SMTP_CLIENT_PASSWORD = os.getenv("SMTP_CLIENT_PASSWORD")

SMTP_GMAIL_CREDENTIALS_PATH = os.getenv("SMTP_GMAIL_CREDENTIALS_PATH", "/app/credentials.json")
SMTP_GMAIL_AUTH_REDIRECT_HOST = os.getenv("SMTP_GMAIL_AUTH_REDIRECT_HOST")
SMTP_GMAIL_AUTH_SERVER_PORT = int(os.getenv("SMTP_GMAIL_AUTH_SERVER_PORT", "8080"))

SMTP_MAILJET_API_KEY = os.getenv("SMTP_MAILJET_API_KEY")
SMTP_MAILJET_API_SECRET = os.getenv("SMTP_MAILJET_API_SECRET")
SMTP_MAILJET_API_VERSION = os.getenv("SMTP_MAILJET_API_VERSION", "v3")

LOG_LEVEL = levelmap.get(os.getenv("LOG_LEVEL", "info").lower(), logging.INFO)

SMTP_SERVICE = os.getenv("SMTP_SERVICE", "smtp")

logging.basicConfig(level=LOG_LEVEL)
