from __future__ import annotations

import shutil


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