from __future__ import annotations
from pathlib import Path
from datetime import datetime


def normalize_input_path(raw: str) -> Path:
    return Path(raw).expanduser().resolve()


def build_output_txt_path(output_dir: Path, audio_path: Path | None) -> Path:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    if audio_path is None:
        stem = "recording"
    else:
        stem = audio_path.stem.replace(" ", "_")

        # Falls der Dateiname bereits mit einem Timestamp beginnt: YYYYMMDD_HHMMSS_
        parts = stem.split("_", 2)
        if len(parts) >= 3 and parts[0].isdigit() and parts[1].isdigit():
            stem = parts[2]  # Entferne den Timestamp-Teil aus dem Stamm
            
    return output_dir / f"{ts}_{stem}.txt"

