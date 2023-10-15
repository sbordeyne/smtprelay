import time

from aiosmtpd.controller import Controller

from smtprelay import config
from smtprelay import auth
from smtprelay.server import SMTPHandler


def main():
    app = Controller(
        SMTPHandler(),
        hostname=config.SMTP_SERVER_HOSTNAME,
        port=config.SMTP_SERVER_PORT,
        decode_data=True,
        enable_SMTPUTF8=True,
        authenticator=auth.callback
    )
    app.start()
    done = False
    while not done:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            print("Shutting down...")
            app.stop()
            done = True


if __name__ == "__main__":
    main()
