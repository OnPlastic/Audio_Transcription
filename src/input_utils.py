from __future__ import annotations

"""
input_utils.py

Utility functions for CLI user interaction.

Responsibilities
----------------
- ask_choice: Prompt the user to select from predefined options.
- ask_email: Prompt the user for a valid email address.
- ask_audio_path: Resolve audio file input and handle retry / fallback flow
"""

from pathlib import Path
from paths import normalize_input_path


def ask_choice(question: str, choices: dict[str, object]) -> object:
    
    """
    Ask the user to choose from predefined options.

    The function keeps prompting until the user enters one of the allowed
    keys. The selected key is mapped to its configured return value.

    Examples
    --------
    {"j": True, "n": False}
    {"s": "save", "m": "mail"}
    
    Parameters
    ----------
    question : str
        The question shown to the user.
    choices : dict[str, object]
        Mapping of valid input options to return values.
    
    Returns
    -------
    object
        The mapped value from the choices dictionary.
    """

    options = "/".join(choices.keys())

    while True:
        answer = input(f"{question} ({options}): ").strip()

        if answer in choices:
            return choices[answer]
        
        print(f"Ungültige Eingabe! Erlaubte Optionen: ({options})")


def ask_email() -> str:
    """
    Ask the user for an email address and validate it.

    The validation is intentionally lightweight and only checks whether
    the input contains both '@' and '.'. This is sufficient for the CLI
    workflow, but not a full RFC-compliant email validation.

    Returns
    -------
    str
        A valid email address entered by the user.
    """

    while True:
        addr = input("Bitte eine gültige E-Mail-Adresse eingeben: ").strip()

        if "@" in addr and "." in addr:
            print("Mailadresse: ", addr)
            return addr
        
        print("Ungültige E-Mail-Adresse! Bitte versuchen Sie es erneut.")


def ask_audio_path(project_root: Path) -> Path | None:
    """
    Ask the user for an audio file, with or without a path, and resolve it.

    If the user enters only a filename, the file is searched for in the 
    default audio directory.

        input/audio/filename.ext

    If the file does not exist, the user can either:
    - retry entering a path or filename
    - switch to the microphone recording flow
    - abort the program

    Parameters
    ----------
    project_root : Path
        The root directory of the project.

    Returns
    -------
    Path | None
        The path to the audio file if found, or None if the user opts to start
        the recorder instead.

    Raises
    ------
    SystemExit
        If the user chooses to abort the program.
    """

    # --- Default: input/audio (Handy-Upload via scp) ---
    default_audio_dir = project_root / "input" / "audio"

    while True:
        raw = input("Bitte Dateiname oder Pfad zur Audio-Datei angeben: ").strip()

        # If only a filename is given, resolve it ralative to input/audio
        if raw and ("/" not in raw) and ("\\" not in raw) and (not raw.startswith("~")):
            audio_path = (default_audio_dir / raw).resolve()
        else:
            audio_path = normalize_input_path(raw)

        if audio_path.exists():
            print("Datei gewählt: ", audio_path)
            return audio_path
        
        print("Datei nicht gefunden: ", audio_path)

        retry = ask_choice(
            "Nochmal versuchen? ",
            {"j": True, "n": False}
        )

        if retry:
            continue

        action = ask_choice(
            "Programm (b)eenden, oder Audio (a)ufnehmen? ",
            {"b": "beenden", "a": "aufnehmen"}
        )

        if action == "beenden":
            raise SystemExit(2)

        # Signal to start the recorder instead of providing a file
        return None
