"""
mail_config.py

Utilities for handling optional mail configuration.

Responsibilities
----------------
- Check whether required SMTP environment variables are present
- Provide a safe way to determine if mail functionality can be used
- Write mail secrets to the .env file
- Update mail-related settings in config.toml
- Test SMTP connection and login credentials

Notes
-----
The mail feature is optional in this project.

Missing configuration must never cause the application to crash.
Instead, the program should fall back to file-based output only.
"""

from __future__ import annotations

import logging
import os
import smtplib
from pathlib import Path


def is_mail_configured() -> bool:
    """
    **Check whether the required mail secrets are available.**

    The mail feature in this project is optional.

    This function checks whether the required environment variables
    for SMTP authentication are present:

        SMTP_USER
        SMTP_APP_PASSWORD

    The check is intentionally lightweight and only verifies that both
    values exist and are non-empty.

    Returns
    -------
        bool
            True if both required mail secrets are available,
            otherwise False.
    """
    return bool(
        os.getenv("SMTP_USER") and os.getenv("SMTP_APP_PASSWORD")
    )


def write_mail_env(
    env_path: Path,
    smtp_user: str,
    smtp_app_password: str,
) -> None:
    """
    **Write the mail secrets to the .env file.**

    This function creates or overwrites the .env file used by the
    project mail configuration.

    The following values are written:

        SMTP_USER
        SMTP_APP_PASSWORD
    
    The file is always written completely new, so previous values 
    in the .env file are replaced.

    Parameters
    ----------
        env_path: Path
            Path to the .env file
        smtp_user: str
            SMTP user name or mail account name.
        smtp_app_password: str
            SMTP app password or mail password used for authentication
    
    Returns
    -------
        None
    """
    content = (
        f'SMTP_USER="{smtp_user}"\n'
        f'SMTP_APP_PASSWORD="{smtp_app_password}"\n'
    )

    env_path.write_text(content, encoding="utf-8")


def update_mail_config(
    config_path: Path,
    smtp_host: str,
    smtp_port: int,
    smtp_use_ssl: bool,
    from_name: str,
    subject_prefix: str,
) -> None:
    """
    **Update the mail-related settings in config.toml.**

    This function updates the existing mail configuration values
    in the project config.toml file

    The following keys are replaced:

        smtp_host
        smtp_port
        smtp_use_ssl
        from_name
        subject_prefix
    
    Only these mail-related keys are updated.
    All other configuration values in config.toml remain unchanged.

    Parameters
    ----------
        config_path: Path
            Path to the config.toml file.
        smtp_host: str
            SMTP server host name.
        smtp_port: int
            SMTP server port.
        smtp_use_ssl: bool
            Whether SSL encryption should be used.
        from_name: str
            Display name used as mail sender name.
        subject_prefix: str
            Prefix used for outgoing mail subjects.
    
    Returns
    -------
        None
    """
    # --- Load file ---
    lines = config_path.read_text(encoding="utf-8").splitlines()

    # --- Prepare new values ---
    replacements = {
        "smtp_host": f'smtp_host = "{smtp_host}"',
        "smtp_port": f"smtp_port = {smtp_port}",
        "smtp_use_ssl": f"smtp_use_ssl = {str(smtp_use_ssl).lower()}",
        "from_name": f'from_name = "{from_name}"',
        "subject_prefix": f'subject_prefix = "{subject_prefix}"',
    }

    new_lines: list[str] = []

    for line in lines:
        stripped = line.strip()

        replaced = False
        for key, new_value in replacements.items():
            if stripped.startswith(f"{key} ="):
                new_lines.append(new_value)
                replaced = True
                break
        
        if not replaced:
            new_lines.append(line)

    # --- Write new file ---
    config_path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")


def test_mail_connection(
        smtp_host: str,
        smtp_port: int,
        smtp_use_ssl: bool,
        smtp_user: str,
        smtp_app_password: str,
) -> bool:
    """
    **Test SMTP connection and login credentials.**

    This function tries to connect to the configured SMTP server
    and authenticate with the provided user credentials.

    No email is sent during this test.

    The test is intended for the interactive mail setup workflow
    and helps detect invalid connection data before saving the
    configuration.

    Parameters
    ----------
        smtp_host: str
            SMTP server host name.
        smtp_port: int
            SMTP server port.
        smtp_use_ssl: bool
            Whether SSL encryption should be used.
        smtp_user: str
            SMTP user name or mail account name.
        smtp_app_password: str
            SMTP app password or mail password used for authentication.
    
    Returns
    -------
        bool
            True if connected and login succeed,
            otherwise False.
    """
    try:
        if smtp_use_ssl:
            server = smtplib.SMTP_SSL(
                smtp_host,
                smtp_port,
                timeout=10,
            )
        else:
            server = smtplib.SMTP(
                smtp_host,
                smtp_port,
                timeout=10,
            )
            server.starttls()
        
        server.login(smtp_user, smtp_app_password)
        server.quit()
        return True
    
    except Exception as exc:
        log = logging.getLogger(__name__)
        log.exception("SMTP Verbindung fehlgeschlagen: %s", exc)
        return False
