from trsc.input_utils import ask_choice, ask_email


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
