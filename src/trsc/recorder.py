from __future__ import annotations

"""
recorder.py

Audio recording utilities for the CLI application.

This module handles microphone recording via sounddevice, converts the
captured float32 audio stream to 16-bit PCM, and stores the result as
a WAV file for later transcription.
"""

import logging
from dataclasses import dataclass
from pathlib import Path
from datetime import datetime
from time import perf_counter

import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write as wav_write

log = logging.getLogger(__name__)


@dataclass(frozen=True)
class RecordingSettings:
    """
    **Audio recording configuration.**
    """

    samplerate: int = 16000
    """The sample rate for recording (16000 Hz)."""
    channels: int = 1
    """The number of audio channels (1 for mono)."""
    dtype: str = "float32"
    """NumPy-compatible audio data type used by sounddevice (float 32)."""


def record_until_enter(
    *,
    output_dir: Path,
    settings: RecordingSettings = RecordingSettings(),
) -> Path:
    """
    **Record audio from the microphone until the user presses ENTER.**

    The recorded audio is stored as a WAV file in the given output
    directory. Internally, the function records float32 audio frames,
    concatenates them after the stream ends, converts them to 16-bit
    PCM, and writes the final WAV file to disk.

    Parameters
    ----------
        output_dir : Path
            The directory where the recorded WAV file will be saved.
        settings : RecordingSettings
            Audio input configuration such as samplerate, channel count,
            and dtype.

    Returns
    -------
        Path
            The path to the saved WAV file.

    Raises
    ------
        RuntimeError
            If no audio data is recorded.
    """

    output_dir.mkdir(parents=True, exist_ok=True)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = output_dir / f"{ts}_recording.wav"

    log.info(
        "Recording started (samplerate=%d, channels=%d) -> %s",
        settings.samplerate,
        settings.channels,
        out_path,
    )

    print("\n-> Aufnahme läuft... Drücke <ENTER> zum Stoppen.")

    frames: list[np.ndarray] = []
    t0 = perf_counter()

    def callback(indata, frame_count, time_info, status):
        """
        Collect incoming audio frames from the sounddevice input stream.
        """

        if status:
            log.warning("Audio status: %s", status)
        frames.append(indata.copy())

    # --- Start audio input stream and stop on ENTER ---
    with sd.InputStream(
        samplerate=settings.samplerate,
        channels=settings.channels,
        dtype=settings.dtype,
        callback=callback,
    ):
        input()  # Wait for ENTER

    dt = perf_counter() - t0

    if not frames:
        raise RuntimeError("Keine Audiodaten aufgenommen (frames leer).")

    # --- Merge all recorded frames into one array ---
    audio = np.concatenate(frames, axis=0)

    # --- Convert float32 audio -> int16 PCM for WAV output ---
    audio = np.clip(audio, -1.0, 1.0)
    audio_i16 = (audio * 32767.0).astype(np.int16)

    wav_write(str(out_path), settings.samplerate, audio_i16)

    seconds = audio.shape[0] / float(settings.samplerate)
    log.info("Recording finished in %.2f s | audio_len=%.2f s", dt, seconds)

    print(f"Aufnahme beendet nach {seconds:.2f} s")
    print(f"Aufnahme gespeichert in: {out_path}")

    return out_path
