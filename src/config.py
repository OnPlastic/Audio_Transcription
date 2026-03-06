from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import tomllib


@dataclass(frozen=True)
class AppConfig:
    output_dir: Path
    log_dir: Path
    log_level: str
    model_name: str
    language: str
    smtp_host: str
    smtp_port: int
    smtp_use_ssl: bool
    from_name: str
    subject_prefix: str


def load_config(project_root: Path) -> AppConfig:
    cfg_path = project_root / "config.toml"

    if not cfg_path.exists():
        raise FileNotFoundError(f"config.toml nicht gefunden: {cfg_path}")

    with cfg_path.open("rb") as f:
        raw = tomllib.load(f)

    transcription_config = raw.get("transcription", {})
    mail_config = raw.get("mail", {})
    logging_config = raw.get("logging", {})

    output_dir = project_root / str(transcription_config.get("output_dir", "output"))
    model_name = str(transcription_config.get("model_name", "large-v3"))
    language = str(transcription_config.get("language", "de"))

    log_dir = project_root / str(logging_config.get("log_dir", "logs"))
    log_level = str(logging_config.get("level", "INFO"))

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

