"""
#🎙️ Audio Transkription CLI

Lightweight command-line application for recording and transcribing
speech using OpenAI Whisper.

------------------------------------------------------------------------

## 1. Project Status

- Python ≥ 3.11
- CLI application
- Whisper speech recognition
- Linux / WSL compatible

------------------------------------------------------------------------

## 2. Features

- Record audio directly from your microphone
- Use existing audio files
- Automatic transcription using Whisper
- Save transcripts as text files
- Optional email delivery
- Structured logging

------------------------------------------------------------------------

## 3. Quick Example

``` pws
    ./run.sh
```

Example output:

``` pws
    Audio_Transkription by sIn vX.X.X
    =================================

    Audio-Datei vorhanden? (j/n): n

    -> Aufnahme läuft...
    -> Transkription startet...

    Transkription beendet in: 9.75 s | Zeichen: 120
    Ergebnis gespeichert in: /output/...txt

    -> Programm beendet
```

------------------------------------------------------------------------

## 4. Installation

Clone repository:

``` pws
    git clone https://github.com/OnPlastic/Audio_Transcription.git
    cd Audio_Transcription
```

Create virtual environment:

``` pws
    python -m venv .venv
    source .venv/bin/activate
```

Install dependencies:

``` pws
    pip install -r requirements.txt
```

Run application:

``` pws
    ./run.sh
```

------------------------------------------------------------------------

## 5. Architecture

```pws
    CLI (main)
      │
      ├── input_utils
      ├── recorder
      ├── whisper_asr
      │
      ├── output
      ├── mailer
      │
      └── logging_setup
```

------------------------------------------------------------------------

## 6. Package Structure

  | Module | Purpose |
  | ------ | ------- |
  | `main` | CLI entry point and workflow orchestration |
  | `config` | Load runtime configuration from `config.toml` |
  | `input_utils` | CLI input helpers and validation |
  | `recorder` | Microphone recording utilities |
  | `whisper_asr` | Whisper transcription wrapper |
  | `output` | Writing transcript files |
  | `mailer` | SMTP email sending |
  | `logging_setup` | Logging configuration |
  | `paths` | Path handling and file naming |
  | `version` | Application metadata |

------------------------------------------------------------------------

## 7. Documentation

API documentation is generated automatically using **pdoc**.

The sidebar lists all available modules and their functions.

------------------------------------------------------------------------

## 👨‍💻 Author

>>```sIn```\n
Project : *Audio_Transkription CLI*

"""

# Import package metadata for external access (e.g., version info)
from .version import APP_NAME, __version__

__all__ = ["APP_NAME", "__version__"]
