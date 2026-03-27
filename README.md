# Audio_Transcription by sIn

![Version](https://img.shields.io/badge/version-1.0.3-blue)
![Tests](https://img.shields.io/badge/tests-17%20passed-brightgreen)
![Python](https://img.shields.io/badge/python-3.12-blue)
[![Ko-fi](https://img.shields.io/badge/-Ko--fi-ff5e5b?logo=ko-fi&logoColor=white)](https://ko-fi.com/onplastic)

## CLI tool for fast, local audio transcription with optional email delivery

This project was developed with a focus on clear architecture, reproducible workflows and clean development processes (GitFlow, testing, documentation)  
German README version available: [Deutsche Version](README_de.md)

---

### ✨ Features

- transcription of audio files (e.g. .wav, .mp3, .m4p)
- optional microphone recording
- output as `.txt` file
- optional delivery via email
- robust CLI input handling (also suitable for SSH / Termux)
- logging into `.log` file
- initial test coverage with `pytest`

---

### ⚡ Example Workflow

```bash
./run.sh
```

**Workflow:**

- specify file or start recording
- start transcription process
- save result within .txt file or forward via email

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

> **Note:** The CLI currently uses German prompts.

---

### 📘 Project Documentation

 Recommended starting point for new users.  
 Full project documentation, including  **installation**, architecture and API-reference, is available via GitHub Pages:

👉 Link: https://onplastic.github.io/Audio_Transcription/

The **README** serves as entry point - details and architecture are described in the documentation.

---

### 🧪 Tests

Tests are executed using `pytest`:

```bash
PYTHONPATH=src pytest
```

Current Status:

- basic tests for core modules are available
- focus on input logic, output, and logging

---

### 📦 Releases

Current Version: **v1.0.2**

Release includes:

- initial testing setup
- baseline tests for core logic
- CLI-input improvements

---

### 👤 Autor

sIn OnPlastic

### ☕ Support

If you like this project or find it helpful, you can buy me a coffee here:

> [![Ko-fi](https://img.shields.io/badge/-Ko--fi-ff5e5b?logo=ko-fi&logoColor=white)](https://ko-fi.com/onplastic)

Thanks a lot, I really appreciate it!
