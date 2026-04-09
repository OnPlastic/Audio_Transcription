from pathlib import Path

from trsc.init_setup import (
    build_default_config_text,
    create_trsc_directories,
    write_config_if_needed,
)


def test_build_default_config_text_contains_required_sections() -> None:
    """
    **Test that the default config text contains the required sections and keys.**
    """

    # Arrange

    # Act
    config_text = build_default_config_text()

    # Assert
    assert "[transcription]" in config_text
    assert 'model_name = "large-v3"' in config_text
    assert 'language = "de"' in config_text
    assert 'output_dir = "output"' in config_text
    assert "[logging]" in config_text
    assert 'log_dir = "logs"' in config_text
    assert 'log_level = "INFO"' in config_text


def test_create_trsc_directories_creates_required_structure(
    tmp_path: Path,
) -> None:
    """
    **Test that the required TRSC directory structure is created.**
    """

    # Arrange
    target_dir = tmp_path / "project-trsc"

    # Act
    target_dir = tmp_path / "project-trsc"

    # Act
    create_trsc_directories(target_dir)

    # Assert
    assert (target_dir / "input").is_dir()
    assert (target_dir / "input" / "audio").is_dir()
    assert (target_dir / "input" / "recordings").is_dir()
    assert (target_dir / "output").is_dir()
    assert (target_dir / "logs").is_dir()


def test_write_config_if_needed_writes_new_config_file(
        tmp_path: Path,
) -> None:
    """
    **Test that config.toml is written if it does not yet exist.**
    """

    # Arrange
    config_path = tmp_path / "config.toml"

    # Act
    written = write_config_if_needed(
        config_path=config_path,
        overwrite_config=False,
    )

    # Assert
    assert written is True
    assert config_path.exists()
    assert "[transcription]" in config_path.read_text(encoding="utf-8")


def test_write_config_if_needed_keeps_existing_file_when_overwrite_is_false(
        tmp_path: Path,
) -> None:
    """
    **Test that an existing config.toml is kept if overwrite is not allowed.**
    """

    # Arrange
    config_path = tmp_path / "config.toml"
    original_text = """[transcription]
    model_name = "tiny"
    """
    config_path.write_text(original_text, encoding="utf-8")

    # Act
    written = write_config_if_needed(
        config_path=config_path,
        overwrite_config=False
    )

    # Assert
    assert written is False
    assert config_path.read_text(encoding="utf-8") == original_text


def test_write_config_if_needed_overwrites_existing_file_when_allowed(
        tmp_path: Path,
) -> None:
    """
    **Test that an existing config.toml is overwritten if approved.**
    """

    # Arrange
    config_path = tmp_path / "config.toml"
    config_path.write_text("old content", encoding="utf-8")

    # Act
    written = write_config_if_needed(
        config_path=config_path,
        overwrite_config=True,
    )

    # Assert
    assert written is True
    assert config_path.read_text(encoding="utf-8") == build_default_config_text()