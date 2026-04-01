# Audio_Transcription by sIn

![Version](https://img.shields.io/badge/version-1.1.3-blue)
![Tests](https://img.shields.io/badge/tests-21%20passed-brightgreen)
![Python](https://img.shields.io/badge/python-3.12-blue)
[![Ko-fi](https://img.shields.io/badge/-Ko--fi-ff5e5b?logo=ko-fi&logoColor=white)](https://ko-fi.com/onplastic)

## CLI tool for fast, local audio transcription with optional email delivery

This project was developed with a focus on clear architecture, reproducible workflows and clean development processes (GitFlow, testing, documentation)  
German README version available: [Deutsche Version](README_de.md)

---

### 1. Features

- transcription of audio files (e.g. .wav, .mp3, .m4p)
- optional microphone recording
- output as `.txt` file
- optional delivery via email (requires additional configuration)
- robust CLI input handling (also suitable for SSH / Termux)
- logging into `.log` file
- initial test coverage with `pytest`

---

### 2. Optional: Mail Configuration

The mail feature is optional.
By default, the tool works without any mail configuration and will only save the transcription as a `.txt` file.  
If no mail configuration is found, the program will automatically fall back to file-only output.

**Setup**

To enable email delivery, run the mail setup tool:

```bash
./run-mail-setup.sh
```

This will:
- ask for SMTP configuration values
- update the mail settings in `config.toml`
- create a `.env` file containing your SMTP credentials  

---

The setup will ask for the following:
- SMTP host (`smtp.gmail.com`)
- SMTP port (`465`)
- SSL usage (j/n)
- sender name (Audio_Transkription by sIn)
- subject prefix ([Transkript])
- SMTP username (musterman@example.com)
- SMTP app password (abc 123)

Notes:
- For Gmail, an App Password is required (2FA must be enabled)
- If you need further information setting up an App Password visit  
  👉 Link: [Gmail-help-pages](https://support.google.com/mail/answer/185833?hl=de&ref_topic=3394217&sjid=4026180072124364108-EU)
- Other providers may require different SMTP settings
- Incorrect configuration will cause the mail delivery to fail  
  -> the transcription will still be saved as a `.txt` file.

---

### 3. Example Workflow

```bash
./run.sh
```

**Workflow:**

- specify file or start recording
- start transcription process
- save result within .txt file or forward via email (if configured)

**Example output:**

``` pws
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

**Note:** The CLI currently uses German prompts.

---

### 4. Project Documentation

 Recommended starting point for new users.  
 Full project documentation, including  **installation**, architecture and API-reference, is available via GitHub Pages:

👉 Link: https://onplastic.github.io/Audio_Transcription/

The **README** serves as entry point - details and architecture are described in the documentation.

---

### 5. Tests

Tests are executed using `pytest`:

```bash
PYTHONPATH=src pytest
```

**Current Status**

- basic tests for core modules are available
- focus on input logic, output, and logging

---

### 6. Releases

Current Version: **v1.1.3**

This release introduces a fully optional and robust mail configuration system.

Release includes:

- Mail functionality is now optional and no longer required for basic usage
- Interactive mail setup tool (`mail_setup.py`) added
- Optional SMTP connection test before saving configuration
- Graceful fallback to file-only output if mail delivery fails
- Improved logging and user feedback during setup and runtime

---

### ✏️ Author

sIn OnPlastic

### ☕ Support

If you like this project or find it helpful, you can buy me a coffee here:

> [![Ko-fi](https://img.shields.io/badge/-Ko--fi-ff5e5b?logo=ko-fi&logoColor=white)](https://ko-fi.com/onplastic)

### 🛠️ Contribute

Want to help improve it? Feel free to contribute 👉 Link: [GitHub](https://github.com/OnPlastic/Audio_Transcription)  

<br>

Thanks a lot ❤️ I really appreciate it! 
