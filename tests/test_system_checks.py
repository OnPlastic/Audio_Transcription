import pytest
from pathlib import Path

from trsc.system_checks import ensure_valid_working_directory
from trsc.recorder import record_until_enter

def test_ensure_valid_working_directory_accepts_minimum_structure(
        tmp_path: Path,
) -> None:
    """
    Accept a valid TRSC working directory with the required minimum structure.
    """

    # Arrange
    (tmp_path / "config.toml").write_text("", encoding="utf-8")
    (tmp_path / "input").mkdir()
    (tmp_path / "output").mkdir()

    # Act
    ensure_valid_working_directory(tmp_path)

    # Assert
    # No exception means success


def test_ensure_valid_working_directory_rejects_missing_output(
        tmp_path: Path,
) -> None:
    """
    Reject working directory if required structure is incomplete.
    """

    # Arrange
    (tmp_path / "config.toml").write_text("", encoding="utf-8")
    (tmp_path / "input").mkdir()
    # output fehlt absichtlich

    # Act & Assert
    with pytest.raises(SystemExit):
        ensure_valid_working_directory(tmp_path)

def test_ensure_valid_working_directory_prints_missing_parts(
        tmp_path: Path,
        capsys,
) -> None:
    """
    Print missing components when structure is invalid.
    """

    # Arrange
    (tmp_path / "config.toml").write_text("", encoding="utf-8")
    # input und output fehlen

    # Act
    with pytest.raises(SystemExit):
        ensure_valid_working_directory(tmp_path)
    
    captured = capsys.readouterr()

    # Assert
    assert "input/" in captured.out
    assert "output/" in captured.out


def test_record_until_enter_fails_without_input_device(
        tmp_path: Path,
        monkeypatch,
) -> None:
    """
    Raise RuntimeError if no input device is available.
    """

    # Arrange
    def fake_query_devices():
        return [
            {"max_input_channels": 0},
            {"max_input_channels": 0},
        ]
    
    import sounddevice as sd
    monkeypatch.setattr(sd, "query_devices", fake_query_devices)

    # Act & Assert
    with pytest.raises(RuntimeError) as exc:
        record_until_enter(output_dir=tmp_path)
    
    assert "Eingabegerät" in str(exc.value)
