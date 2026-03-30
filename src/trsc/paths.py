"""
paths.py

Utility functions for handling filesystem paths used by the CLI application.

Responsibilities
----------------
- Normalize user provided input paths
- Generate output file paths for transcripts
"""

from __future__ import annotations

from pathlib import Path
from datetime import datetime


def normalize_input_path(raw: str) -> Path:
    """
    **Normalize a user-provided path string.**

    This expands user home shortcuts (~) and resolves the absolute path.

    Parameters
    ----------
    raw: str
        Raw path string entered by the user.

    Returns
    -------
    Path
        Normalized absolute path.
    """

    return Path(raw).expanduser().resolve()


def build_output_txt_path(output_dir: Path, audio_path: Path | None) -> Path:
    """
    **Build the output path for the transcript text file.**

    The generated filename always begins with a timestamp:

        YYYYMMDD_HHMMSS_<stem>.txt

        If the audio filename already contains a timestamp prefix,
        it will be removed from the stem to avoid duplication.

    Example
    -------
    Input:
        20260601_153000_recording.wav

    Output:
        20260601_153000_recording.txt

    Parameters
    ----------
        output_dir: Path
            Directory where the transcript should be saved.
        audio_path: Path | None
            Path to the audio file used for transcription.
            If None, the default stem "recording" will be used.

    Returns
    -------
        Path
            Full path for the output transcript text file.
    """

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    if audio_path is None:
        stem = "recording"
    else:
        stem = audio_path.stem.replace(" ", "_")

        # Remove existing timestamp prefix from the stem if present
        parts = stem.split("_", 2)

        if len(parts) >= 3 and parts[0].isdigit() and parts[1].isdigit():
            stem = parts[2]

    return output_dir / f"{ts}_{stem}.txt"
