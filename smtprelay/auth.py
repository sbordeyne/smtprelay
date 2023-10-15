from aiosmtpd.smtp import AuthResult


def callback(server, session, envelope, mechanism, auth_data) -> AuthResult:
    """
    Dummy callback for SMTP authentication. Regardless of the credentials,
    it'll authenticate. Designed for intra-kube relaying, so external IPs don't
    have access to the SMTP server anyways.
    """
    return AuthResult(
        success=True,
        handled=True,
        message=None,
        auth_data=None,
    )
