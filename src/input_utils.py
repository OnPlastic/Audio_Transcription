from __future__ import annotations

from pathlib import Path
from paths import normalize_input_path


def ask_choice(question: str, choices: dict[str, object]) -> object:
    
    """
    Ask the user to choose from predefined options.
    
    Parameters
    ----------
    question : str
        The question shown to the user.
    choices : dict[str, object]
        Mapping of valid input options to return values.
        
        Example:
        {"j": True, "n": False}
        {"s": "save", "m": "mail"}
    
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
    Ask the user for an audio file, with a default directory for convenience.
    If only a filename is provided, it will be searched for in the default 
    input/audio directory.

    Returns
    -------
    Path | None
        The path to the audio file if found, or None if the user opts to start
        the recorder instead.
    """

    # --- Default: input/audio (für Handy-Upload via scp) ---
    default_audio_dir = project_root / "input" / "audio"

    while True:
        raw = input("Bitte Dateiname oder Pfad zur Audio-Datei angeben: ").strip()

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

        return None  # Signal to start the recorder instead of providing a file
