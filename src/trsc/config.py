from __future__ import annotations

"""
config.py

Loads runtime configuration from config.toml and exposes it as a typed
AppConfig object for the CLI application.
"""

from dataclasses import dataclass
from pathlib import Path
import tomllib


@dataclass(frozen=True)
class AppConfig:
    """
    **Application runtime configuration loaded from config.toml.**
    """

    output_dir: Path
    """ Directory where transcriptions will be saved."""
    log_dir: Path
    """ Directory where log files will be stored."""
    log_level: str
    """ Logging level (e.g. "INFO", "DEBUG")."""
    model_name: str
    """ Name of the Whisper model to use (large-v3)."""
    language: str
    """ Language code given to Whisper for transcription (de)."""
    smtp_host: str
    """ SMTP server host for sending emails."""
    smtp_port: int
    """ SMTP server port (465 for SSL, 587 for TLS)."""
    smtp_use_ssl: bool
    """ Whether to use SSL for SMTP connection."""
    from_name: str
    """ Display name for the sender in the email."""
    subject_prefix: str
    """ Prefix for the email subject line ([Transkript])."""


def load_config(project_root: Path) -> AppConfig:
    """
    **Load application settings from config.toml
    located in the project root directory.**

    Values are grouped into the sections:
    - transcription: output_dir, model_name, language
    - mail: smtp_host, smtp_port, smtp_use_ssl, from_name, subject_prefix
    - logging: log_dir, level

    Missing values are replaced with defaults.
    The resulting AppConfig object is returned.

    Parameters
    ----------
        project_root: Path
            Root directory of the project where config.toml is located.

    Returns
    -------
        AppConfig
            Parsed and normalized runtime configuration.
    """

    cfg_path = project_root / "config.toml"

    if not cfg_path.exists():
        raise FileNotFoundError(f"config.toml nicht gefunden: {cfg_path}")

    # --- Load raw TOML data ---
    with cfg_path.open("rb") as f:
        raw = tomllib.load(f)

    # --- Extract configuration sections ---
    transcription_config = raw.get("transcription", {})
    mail_config = raw.get("mail", {})
    logging_config = raw.get("logging", {})

    # --- Transcription settings ---
    output_dir = project_root / str(
        transcription_config.get("output_dir", "output")
    )
    model_name = str(transcription_config.get("model_name", "large-v3"))
    language = str(transcription_config.get("language", "de"))

    # --- Logging settings ---
    log_dir = project_root / str(logging_config.get("log_dir", "logs"))
    log_level = str(logging_config.get("level", "INFO"))

    # --- Mail settings ---
    smtp_host = str(mail_config.get("smtp_host", "smtp.gmail.com"))
    smtp_port = int(mail_config.get("smtp_port", 465))
    smtp_use_ssl = bool(mail_config.get("smtp_use_ssl", True))
    from_name = str(mail_config.get("from_name", "Spracherkennung by sIn"))
    subject_prefix = str(mail_config.get("subject_prefix", "[Transkript]"))

    return AppConfig(
        output_dir=output_dir,
        log_dir=log_dir,
        log_level=log_level,
        model_name=model_name,
        language=language,
        smtp_host=smtp_host,
        smtp_port=smtp_port,
        smtp_use_ssl=smtp_use_ssl,
        from_name=from_name,
        subject_prefix=subject_prefix
    )
