"""
mailer.py

Email delivery utilities for the CLI application.

this module builds and sends plain text emails containing the generated
transcript. SMTP settings are provided through the SmtpSettings dataclass.
"""

from __future__ import annotations

import logging
import smtplib
from dataclasses import dataclass
from email.message import EmailMessage

log = logging.getLogger(__name__)


@dataclass(frozen=True)
class SmtpSettings:
    """
    **SMTP configuration used for outgoing emails.**
    """

    host: str
    """ The SMTP server hostname or IP address."""
    port: int
    """ The port number to connect to on the SMTP server."""
    use_ssl: bool
    """ Whether to use SSL/TLS for the connection."""
    user: str
    """ SMTP login username / sender address."""
    app_password: str
    """ SMTP login password or app-specific password."""
    from_name: str
    """ Display name to use in the "From" field of outgoing emails."""


def send_mail_text(
    *,
    smtp: SmtpSettings,
    to_addr: str,
    subject: str,
    text_content: str,
) -> None:
    """
    Send a plan text email containing a transcript.

    The transcript is embedded directly in teh email body, Depending on the
    SMTP configuration, the function either connects via SMTP over SSL or
    via SMTP + STARTTLS.

    Parameters
    ----------
        smtp : SmtpSettings
            SMTP connection and sender configuration.
        to_addr : str
            Recipient email address.
        subject : str
            Subject line for the email.
        text_content : str
            The transcript text to include in the email body.

    Returns
    -------
        None
    """

    # --- Build the email message ---
    msg = EmailMessage()
    msg["From"] = f"{smtp.from_name} <{smtp.user}>"
    msg["To"] = to_addr
    msg["Subject"] = subject

    # --- Build plain text mail body ---
    body = f"""Erfasster Text:
---
{text_content}
---
"""
    msg.set_content(body)

    log.info("Sending mail to=%s subject=%s", to_addr, subject)

    # --- Send email using configured SMTP transport ---
    if smtp.use_ssl:
        with smtplib.SMTP_SSL(smtp.host, smtp.port) as server:
            server.login(smtp.user, smtp.app_password)
            server.send_message(msg)
    else:
        with smtplib.SMTP(smtp.host, smtp.port) as server:
            server.starttls()
            server.login(smtp.user, smtp.app_password)
            server.send_message(msg)

    log.info("Mail sent to %s", to_addr)
