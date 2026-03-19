import logging
from pathlib import Path

from trsc.logging_setup import setup_logging


def test_setup_logging_creates_log_file(tmp_path: Path) -> None:
    # Arrange
    log_dir = tmp_path / "logs"

    # Act
    logfile = setup_logging(log_dir)

    # Assert
    assert logfile.exists()
    assert logfile.parent == log_dir
    assert logfile.suffix == ".log"


def test_setup_logging_writes_initial_log_entry(tmp_path: Path) -> None:
    # Arrange
    log_dir = tmp_path / "logs"

    # Act
    logfile = setup_logging(log_dir)

    # Read file content
    content = logfile.read_text(encoding="utf-8")

    # Assert
    assert "Logging initialized" in content


def test_setup_logging_replaces_existing_handlers(tmp_path: Path) -> None:
    # Arrange
    root = logging.getLogger()
    old_handler = logging.StreamHandler()
    root.addHandler(old_handler)

    log_dir = tmp_path / "logs"

    # Act
    setup_logging(log_dir)

    # Assert
    assert old_handler not in root.handlers
    assert len(root.handlers) == 1
    assert isinstance(root.handlers[0], logging.FileHandler)


