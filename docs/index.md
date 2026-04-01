# 🎙️ Audio Transkription by sIn

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
- Optional email delivery (additional Setup required)
- Structured logging

------------------------------------------------------------------------

## 3. Quick Example

```bash
    ./run.sh
```

**Example output:**

```bash
    Audio_Transkription by sIn vX.X.X
    =================================

    Audio-Datei vorhanden? (j/n): n

    -> Aufnahme läuft...
    -> Transkription startet...

    Transkription beendet in: 9.75 s | Zeichen: 120
    Ergebnis gespeichert in: /output/...txt
    Mail versandt an: ...

    -> Programm beendet
```
-------------------------------------------------------------------------

## 4. System Requirements

This project requires **ffmpeg** for audio decoding used by Whisper.

**Install on Linux/WSL:**

```bash
    sudo apt update
    sudo apt install ffmpeg
```

**Verify installation:**

```bash
    ffmpeg -version
```

------------------------------------------------------------------------

## 5. Installation

**Clone repository:**

```bash
    git clone https://github.com/OnPlastic/Audio_Transcription.git
    cd Audio_Transcription
```

**Create virtual environment:**

```bash
    python -m venv .venv
    source .venv/bin/activate
```

**Install runtime dependencies:**

```bash
    pip install -r requirements.txt
```

**Note!** (Ubuntu / WSL users)

>  
> Some Ubuntu installations do not provide the ` python ` command by default. If ` python -m venv .venv ` fails with ` command not found ` Error, use:  
>
>   `python3 -m venv .venv`
>
> Or install the compatibility package once:
>
>   `sudo apt install python-is-python3`  
><br>

*Optional:* (install development tools / documentation & linting)

```bash
    pip install -r requirements-dev.txt
```

**Run application:**

```bash
    ./run.sh
```

------------------------------------------------------------------------
## 6. Mail Configuration

The mail feature is optional.

By default, the application works without any mail configuration and
will only save the transcription as a `.txt` file.

If no mail configuration is present, the program will automatically
fall back to file-only output.

### Setup

**Run the mail setup tool:**

```bash
    ./run-mail-setup.sh
```

**The setup will:**

- ask for SMTP configuration values
- update mail settings in `config.toml`
- create a `.env` file containing SMTP credentials

**Configuration Values asked in the Setup:**

- SMTP host (`smtp.gmail.com`)
- SMTP port (`465`)
- SSL usage (j/n)
- sender name (Audio_Transkription by sIn)
- subject prefix ([Transkript])
- SMTP username (musterman@example.com)
- SMTP app password (abc 123)

**Notes:**

- For Gmail, an App Password is required (2FA must be enabled)
- If you need further information setting up an App Password visit  
  👉 Link: [Gmail-help-pages](https://support.google.com/mail/answer/185833?hl=de&ref_topic=3394217&sjid=4026180072124364108-EU)
- Other providers may require different SMTP settings
- Incorrect configuration will cause the mail delivery to fail  
  -> the transcription will still be saved as a `.txt` file.
 
------------------------------------------------------------------------

## 7. Architecture

```bash
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

>A more detailed Version of all Packages and Modules are here available, open:
>👉 Link: [**trsc-architecture-diagram**](assets/TRSC.svg)

------------------------------------------------------------------------

## 8. Package Structure

| Module | Purpose |  
| :----- | :------ |  
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

## 9. Documentation

API documentation is generated using **pdoc**.

The landing page of the documentation is generated from the `trsc`
module docstring and contains the project overview.

The sidebar lists all available modules and their functions.

------------------------------------------------------------------------

## 👨‍💻 Author

>   ```sIn```- OnPlastic  
Project : *Audio_Transkription CLI*


### ☕ Support

If you like this project or find it helpful, you can buy me a coffee here:

[![Ko-fi](https://img.shields.io/badge/-Ko--fi-ff5e5b?logo=ko-fi&logoColor=white)](https://ko-fi.com/onplastic)

### 🛠️ Contribute

Want to help improve it? Feel free to contribute 👉 Link: [GitHub](https://github.com/OnPlastic/Audio_Transcription)  

<br>

Thanks a lot ❤️ I really appreciate it! 
