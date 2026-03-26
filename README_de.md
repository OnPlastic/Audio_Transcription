# Audio_Transcription by sIn

![Version](https://img.shields.io/badge/version-1.0.3-blue)
![Tests](https://img.shields.io/badge/tests-17%20passed-brightgreen)
![Python](https://img.shields.io/badge/python-3.12-blue)

## CLI-Tool zur lokalen Transkription von Audio-Dateien mit optionalem Versand per E-Mail.

Dieses Projekt wurde mit Fokus auf klare Architektur, reproduzierbare Workflows und saubere Entwicklungsprozesse (GitFlow, Testing, Dokumentation) entwickelt.

---

## ✨ Features

- Transkription von Audio-Dateien
- Optionale Aufnahme über Mikrofon
- Ausgabe als `.txt` Datei
- Optionaler Versand per E-Mail
- Robuste CLI-Eingabelogik (auch für SSH / Termux geeignet)
- Logging in Datei `.log`
- Erste Testabdeckung mit `pytest`

---

## ⚡ Beispiel Workflow

```bash
./run.sh
```

**Ablauf:**

- Datei angeben oder Aufnahme starten
- Transkription durchführen
- Ergebnis speichern oder per Mail versenden

**Beispielausgabe:**

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

---

## 📘 Projektdokumentation

Die vollständige Projektdokumentation, einschließlich **Installation**, Architektur und API-Referenz, ist auf GitHub Pages verfügbar:

- Link: https://onplastic.github.io/Audio_Transcription/

Die **README** dient als Einstiegspunkt – Details und Architektur sind in der Doku beschrieben.

---

## 🧪 Tests

Tests werden mit `pytest` ausgeführt:

```bash
PYTHONPATH=src pytest
```

Aktueller Stand:

- Basistests für Kernmodule vorhanden
- Fokus auf Eingabelogik, Output und Logging

---

## 📦 Releases

Aktuelle Version: **v1.0.2**

Release enthält:

- initiales Testing-Setup
- Basistests für Kernlogik
- Verbesserungen an CLI-Eingaben

---

## 👤 Autor

sIn OnPlastic
