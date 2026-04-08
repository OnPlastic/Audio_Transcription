from __future__ import annotations

import shutil

from pathlib import Path


def ensure_ffmpeg_available() -> None:
    """
    Ensure that ffmpeg is available in PATH.

    Aborts the programm with clear message if ffmpeg is missing.
    """

    if shutil.which("ffmpeg") is None:
        print("FFmpeg wurde nicht gefunden.")
        print("Dieses Tool benötigt FFmpeg zur Audioverarbeitung.\n")
        print("Bitte installiere FFmpeg und starte das Programm erneut.")
        print("Ubuntu/Debian: sudo apt install ffmpeg\n")
        raise SystemExit(1)


def ensure_valid_working_directory(project_root: Path) -> None:
    """
    Ensure that the current working directory is a valid TRSC project directory.

    Required structure:
    - config.toml
    - input/
    - output/
    """

    missing = []

    if not (project_root / "config.toml").exists():
        missing.append("config.toml")
    
    if not (project_root / "input").is_dir():
        missing.append("input/")
    
    if not (project_root / "output").is_dir():
        missing.append("output/")
    
    if missing:
        print("Ungültiges TRSC-Arbeitsverzeichnis.\n")
        print("Folgende Bestandteile fehlen:")
        for item in missing:
            print(f" - {item}")
        
        print("\nBitte führe 'trsc' im Projektordner aus,")
        print("oder stelle sicher dass die TRSC-Struktur vorhanden ist.\n")

        raise SystemExit(1)