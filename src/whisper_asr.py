from __future__ import annotations

"""
whisper_asr.py

Speech-to-Text utilities based on OpenAI's Whisper model.

This module loads and caches the configured Whisper model and provides
a helper function to transcribe audio files into plain text.
"""

import logging
from pathlib import Path
from time import perf_counter

import whisper

log = logging.getLogger(__name__)

# Cached Whisper model instance and its configured model name
_MODEL = None
_MODEL_NAME = None


def get_model(model_name: str):
    """
    Load and cache a Whisper model by name.

    If the requested model has already been loaded previously, the cached
    instance is returned. If a different model name is requested, the cache
    is replaced with the newly loaded model.

    Parameters
    ----------
    model_name : str
        The name of the Whisper model to load (e.g., "large-v3").

    Returns
    -------
    object
        The loaded Whisper model instance.
    """

    global _MODEL, _MODEL_NAME

    if _MODEL is None or _MODEL_NAME != model_name:
        log.info("Loading Whisper model: %s", model_name)
        _MODEL = whisper.load_model(model_name)
        _MODEL_NAME = model_name
        log.info("Whisper model loaded: %s", model_name)

    return _MODEL


def transcribe_file(audio_path: Path, model_name: str, language: str) -> str:
    """
    Transcribe an audio file using Whisper.

    The function ensures that the configured model is available, runs a
    transcription in the specified language, and returns the resulting
    plain text.

    Parameters
    ----------
    audio_path : Path
        The path to the audio file to transcribe.
    model_name : str
        The name of the Whisper model to use for transcription.
    language : str
        The language code passed to Whisper (de).

    Returns
    -------
    str
        The transcribed plain text.
    
    Raises    
    ------
    FileNotFoundError
        If the specified audio file does not exist.
    """

    if not audio_path.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    model = get_model(model_name)

    log.info("Transcription started: %s", audio_path)
    t0 = perf_counter()

    # fp16 is usually only useful on GPU; on CPU it may causes issues
    result = model.transcribe(
        str(audio_path),
        language=language,
        task="transcribe",
        fp16=False,
    )

    dt = perf_counter() - t0
    text = str(result.get("text", "")).strip()

    log.info("Transcription finished in %.2f s | chars=%d", dt, len(text))

    print(f"Transkription beendet in: {dt:.2f} s | Zeichen: {len(text)}")

    return text
