from pathlib import Path

from trsc.mail_config import is_mail_configured, write_mail_env, update_mail_config

import pytest


def test_mail_config_missing(monkeypatch):
    """
    Mail config should be False if environment variables are missing.
    """
    # Arrange
    monkeypatch.delenv("SMTP_USER", raising=False)
    monkeypatch.delenv("SMTP_APP_PASSWORD", raising=False)

    # Act
    result = is_mail_configured()

    # Assert
    assert result is False


def test_mail_config_present(monkeypatch):
    """
    Mail config should be True if both environment variables are set.
    """
    # Arrange
    monkeypatch.setenv("SMTP_USER", "test@example.com")
    monkeypatch.setenv("SMTP_APP_PASSWORD", "dummy-password")

    # Act
    result = is_mail_configured()

    # Assert
    assert result is True


def test_write_mail_env_creates_expected_content(tmp_path: Path) -> None:
    """
    
    """
    # Arrange
    env_path = tmp_path / ".env"

    smtp_user = "test@example.com"
    smtp_app_password = "abc 123"

    # Act
    write_mail_env(
        env_path=env_path,
        smtp_user=smtp_user,
        smtp_app_password=smtp_app_password,
    )

    # Assert
    content = env_path.read_text(encoding="utf-8")

    expected = (
        'SMTP_USER="test@example.com"\n'
        'SMTP_APP_PASSWORD="abc 123"\n'
    )

    assert content == expected


def test_update_mail_config_replaces_only_mail_fields(tmp_path: Path) -> None:
    # Arrange
    config_path = tmp_path / "config.toml"

    original_content = """
[Mail]
smtp_host = "old_host"
smtp_port = 123
smtp_use_ssl = true
from_name = "old_name"
subject_prefix = "old_prefix

[other]
some_value = 42
""".strip()
    
    config_path.write_text(original_content, encoding="utf-8")

    # Act
    update_mail_config(
        config_path=config_path,
        smtp_host="smtp.new.com",
        smtp_port=400,
        smtp_use_ssl=False,
        from_name="new_name",
        subject_prefix="new_prefix",
    )

    # Assert
    updated = config_path.read_text(encoding="utf-8")

    assert 'smtp_host = "smtp.new.com"' in updated
    assert "smtp_port = 400" in updated
    assert "smtp_use_ssl = false" in updated
    assert 'from_name = "new_name"' in updated
    assert 'subject_prefix = "new_prefix"' in updated

    # Other values should be untouched
    assert "some_value = 42" in updated
