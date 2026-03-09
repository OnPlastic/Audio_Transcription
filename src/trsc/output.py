from __future__ import annotations

"""
output.py

Output utilities for writing generated transcript files to disk.
"""

from pathlib import Path


def write_txt(path: Path, content: str) -> None:
    """
    **Write transcript text to a UTF-8 encoded text file.**

    The parent directory is created if it does not yet exist.

    Parameters
    ----------
        path : Path
            Full path to the output text file.
        content : str
            Transcript text to write to the file.

    Returns
    -------
        None
    """

    # --- Ensure output directory exists ---
    path.parent.mkdir(parents=True, exist_ok=True)

    # --- Write transcript text to file ---
    path.write_text(content, encoding="utf-8")
