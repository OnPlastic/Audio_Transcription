from pathlib import Path

from trsc.input_utils import ask_choice, ask_email, ask_audio_path


def test_ask_choice_returns_mapped_value_for_valid_input(monkeypatch) -> None:
    # Arrange
    def fake_prompt_input(prompt: str) -> str:
        return "j"
    
    monkeypatch.setattr("trsc.input_utils.prompt_input", fake_prompt_input)

    # Act
    result =  ask_choice("Weiter?", {"j": True, "n": False})

    # Assert
    assert result is True


def test_ask_choice_retries_until_valid_input(monkeypatch) -> None:
    # Arrange
    answers = iter(["x", "n"])

    def fake_prompt_input(prompt: str) -> str:
        return next(answers)
    
    monkeypatch.setattr("trsc.input_utils.prompt_input", fake_prompt_input)

    # Act
    result = ask_choice("Weiter?", {"j": True, "n": False})

    # Assert
    assert result is False


def test_ask_choice_prints_error_on_invalid_input(monkeypatch, capsys) -> None:
    # Arrange
    answers = iter(["x", "j"])

    def fake_prompt_input(prompt: str) -> str:
        return next(answers)
    
    monkeypatch.setattr("trsc.input_utils.prompt_input", fake_prompt_input)

    # Act
    result = ask_choice("Weiter?", {"j": True, "n": False})

    # Capture output
    captured = capsys.readouterr()

    # Assert
    assert "Ungültige Eingabe" in captured.out
    assert result is True


def test_ask_email_returns_valid_email(monkeypatch) -> None:
    # Arrange
    def fake_prompt_input(prompt: str) -> str:
        return "test@example.com"
    
    monkeypatch.setattr("trsc.input_utils.prompt_input", fake_prompt_input)

    # Act
    result = ask_email()

    # Assert
    assert result == "test@example.com"


def test_ask_email_retries_until_valid_email(monkeypatch, capsys) -> None:
    # Arrange
    answers = iter(["abc", "test@example.com"])

    def fake_prompt_input(prompt: str) -> str:
        return next(answers)
    
    monkeypatch.setattr("trsc.input_utils.prompt_input", fake_prompt_input)

    # Act
    result = ask_email()
    captured = capsys.readouterr()

    # Assert
    assert "Ungültige E-Mail-Adresse" in captured.out
    assert result == "test@example.com"


def test_ask_audio_path_returns_file_from_default_audio_dir(
        monkeypatch, tmp_path: Path
) -> None:
    # Arrange
    project_root = tmp_path
    audio_dir = project_root / "input" / "audio"
    audio_dir.mkdir(parents=True)

    expected_path = (audio_dir / "sample.wav").resolve()
    expected_path.write_text("dummy", encoding="utf-8")

    def fake_prompt_input(prompt: str) -> str:
        return "sample.wav"

    monkeypatch.setattr("trsc.input_utils.prompt_input", fake_prompt_input)

    # Act
    result = ask_audio_path(project_root)

    # Assert
    assert result == expected_path


def test_ask_audio_path_retry_until_valid(
        monkeypatch, tmp_path: Path
) -> None:
    # Arrange
    project_root = tmp_path
    audio_dir = project_root / "input" / "audio"
    audio_dir.mkdir(parents=True)

    valid_path = (audio_dir / "valid.wav").resolve()
    valid_path.write_text("dummy", encoding="utf-8")

    inputs = iter(["wrong.wav", "j", "valid.wav"])

    def fake_prompt_input(prompt: str) -> str:
        return next(inputs)
    
    monkeypatch.setattr("trsc.input_utils.prompt_input", fake_prompt_input)

    # Act
    result = ask_audio_path(project_root)

    # Assert
    assert result == valid_path


def test_ask_audio_path_returns_none_for_recorder_flow(
        monkeypatch, tmp_path: Path
) -> None:
    # Arrange
    project_root = tmp_path
    inputs = iter(["wrong.wav", "n", "a"])

    def fake_prompt_input(prompt: str) -> str:
        return next(inputs)
    
    monkeypatch.setattr("trsc.input_utils.prompt_input", fake_prompt_input)

    # Act
    result = ask_audio_path(project_root)

    # Assert
    assert result is None


import pytest


def test_ask_audio_path_exits_on_user_abort(
    monkeypatch, tmp_path: Path
) -> None:
    # Arrange
    project_root = tmp_path
    inputs = iter(["wrong.wav", "n", "b"])

    def fake_prompt_input(prompt: str) -> str:
        return next(inputs)

    monkeypatch.setattr("trsc.input_utils.prompt_input", fake_prompt_input)

    # Act + Assert
    with pytest.raises(SystemExit):
        ask_audio_path(project_root)


def test_ask_audio_path_retries_on_empty_input(
        monkeypatch, tmp_path: Path, capsys
) -> None:
    #Arrange
    project_root = tmp_path
    audio_dir = project_root / "input" / "audio"
    audio_dir.mkdir(parents=True)

    expected_path = (audio_dir / "valid.wav").resolve()
    expected_path.write_text("dummy", encoding="utf-8")

    inputs = iter(["", "valid.wav"])

    def fake_prompt_input(prompt: str) -> str:
        return next(inputs)
    
    monkeypatch.setattr("trsc.input_utils.prompt_input", fake_prompt_input)

    # Act
    result = ask_audio_path(project_root)
    captured = capsys.readouterr()

    # Assert
    assert "Keine Eingabe erkannt" in captured.out
    assert result == expected_path