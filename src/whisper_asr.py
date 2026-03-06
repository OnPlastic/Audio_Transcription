from __future__ import annotations
from time import perf_counter
import logging
from pathlib import Path
import whisper


log = logging.getLogger(__name__)

_MODEL = None
_MODEL_NAME = None


def get_model(model_name: str):
    global _MODEL, _MODEL_NAME

    if _MODEL is None or _MODEL_NAME != model_name:
        log.info("Loading Whisper model: %s", model_name)
        _MODEL = whisper.load_model(model_name)
        _MODEL_NAME = model_name
        log.info("Whisper model loaded: %s", model_name)

    return _MODEL


def transcribe_file(audio_path: Path, model_name: str, language: str) -> str:
    """
    Transkribiert eine Audiodatei mit Whisper.
    - Modell: large-v3
    - Sprache: Deutsch (de)
    - Output: reiner TEXT
    """
    if not audio_path.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    model = get_model(model_name)

    log.info("Transcription started: %s", audio_path)
    t0 = perf_counter()
    # fp16 nur auf GPU sinnvoll; auf CPU kann fp16 Probleme machen
    result = model.transcribe(
        str(audio_path),
        language=language,
        task="transcribe",
        fp16=False,
    )

    dt = perf_counter() - t0
    text = str(result.get("text", "")).strip()
    log.info("Transcription finished in %.2f s | chars=%d", dt, len(text))
    return text
