# SMTP Relay

Simple mail relay to use inside of a kubernetes cluster (it has no authentication, be warned, do not expose to the internet!)

## Setup

| Variable                      | Value / Example       | Description                                                  |
|-------------------------------|-----------------------|--------------------------------------------------------------|
| SMTP_SERVICE                  | smtp/mailjet/google   | The service to use to forward mail to                        |
| SMTP_SERVER_HOSTNAME          | 0.0.0.0               | Bind address of the builtin SMTP server                      |
| SMTP_SERVER_PORT              | 8025                  | Listening port of the builtin SMTP server                    |
| SMTP_CLIENT_HOSTNAME          | smtp.google.com       | (smtp) Host of the SMTP server to forward to                 |
| SMTP_CLIENT_PORT              | 465                   | (smtp) Port of the SMTP server to forward to                 |
| SMTP_CLIENT_USE_SSL           | true                  | (smtp) Whether to use SSL or not                             |
| SMTP_CLIENT_USE_AUTH          | false                 | (smtp) Whether the server needs authentication               |
| SMTP_CLIENT_LOGIN             | john.doe@gmail.com    | (smtp) if USE_AUTH, login of the SMTP server                 |
| SMTP_CLIENT_PASSWORD          | P4s$W0rd              | (smtp) if USE_AUTH, password for the SMTP server             |
| SMTP_GMAIL_CREDENTIALS_PATH   | /app/credentials.json | (google) Path to the credentials file for google OAuth2 flow |
| SMTP_GMAIL_AUTH_REDIRECT_HOST | example.com           | (google) Host used for the redirection after the OAuth2 flow |
| SMTP_GMAIL_AUTH_SERVER_PORT   | 8080                  | (google) Port the auth HTTP server listens on.               |
| SMTP_MAILJET_API_KEY          | xxx                   | (mailjet) MailJet API Key                                    |
| SMTP_MAILJET_API_SECRET       | xxxx                  | (mailjet) MailJet API Secret                                 |
| SMTP_MAILJET_API_VERSION      | v3                    | (mailjet) MailJet API version (v3, v3.1)                     |
| LOG_LEVEL                     | debug/info/warn/error | Log level of the app                                         |

