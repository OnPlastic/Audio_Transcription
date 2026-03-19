from pathlib import Path
from trsc.output import write_txt


def test_write_txt_creates_file(tmp_path: Path) -> None:
    # Arrange (Vorbereitung)
    test_text = "Hallo Test"
    file_path = tmp_path / "output" / "test.txt"

    # Act (Aktion)
    write_txt(file_path, test_text)

    # Assert (Überprüfung)
    assert file_path.exists()

def test_write_txt_writes_expected_content(tmp_path: Path) -> None:
    # Arrange
    test_text = "Hallo Test"
    file_path = tmp_path / "output" / "test.txt"

    # Act
    write_txt(file_path, test_text)

    # Assert
    assert file_path.read_text(encoding="utf-8") == test_text

def test_write_txt_creates_parent_directory(tmp_path: Path) -> None:
    # Arrange
    test_text = "Hallo Test"
    file_path = tmp_path / "nested" / "output" / "test.txt"

    assert not file_path.parent.exists()

    # Act
    write_txt(file_path, test_text)

    # Assert
    assert file_path.parent.exists()
    assert file_path.parent.is_dir()