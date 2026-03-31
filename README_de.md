# Audio_Transcription by sIn

![Version](https://img.shields.io/badge/version-1.1.2-blue)
![Tests](https://img.shields.io/badge/tests-17%20passed-brightgreen)
![Python](https://img.shields.io/badge/python-3.12-blue)
[![Ko-fi](https://img.shields.io/badge/-Ko--fi-ff5e5b?logo=ko-fi&logoColor=white)](https://ko-fi.com/onplastic)

## CLI-Tool zur lokalen Transkription von Audio-Dateien mit optionalem Versand per E-Mail.

Dieses Projekt wurde mit Fokus auf klare Architektur, reproduzierbare Workflows und saubere Entwicklungsprozesse (GitFlow, Testing, Dokumentation) entwickelt.

---

### 1. Features

- Transkription von Audio-Dateien
- Optionale Aufnahme über Mikrofon
- Ausgabe als `.txt` Datei
- Optionaler Versand per E-Mail
- Robuste CLI-Eingabelogik (auch für SSH / Termux geeignet)
- Logging in Datei `.log`
- Erste Testabdeckung mit `pytest`

---
### 2. Option: Email Einrichtung 

Die Mail-Funktion ist optional.  
Standardmäßig arbeitet das Tool ohne jegliche Mail-Konfiguration und speichert die Transkription nur als `.txt`-Datei. Wenn keine Mail-Konfiguration gefunden wird, fällt das Programm automatisch auf die Datei-Ausgabe zurück.

**Setup**

Um den E-Mail Funktion zu aktiviren, bitte das mail-setup-tool ausführen:

```bash
./run-mail-setup.sh
```

Dies wird:
- nach SMTP-Konfigurationswerten fragen
- die E-Mail-Einstellungen in der `config.toml` aktualisieren
- eine `.env`-Datei mit Ihren SMTP-Zugangsdaten erstellen  

---

Im Setup werden folgende Parameter eingestellt:
- SMTP host (`smtp.gmail.com`)
- SMTP port (`465`)
- SSL usage (j/n)
- sender name (Audio_Transkription by sIn)
- subject prefix ([Transkript])
- SMTP username (musterman@example.com)
- SMTP app password (abc 123)

Anmerkungen:
- Für Gmail wird ein App-Passwort benötigt (2FA muss aktiviert sein)
- Wenn Sie weitere Informationen zum Einrichten eines App-Passworts benötigen, besuchen Sie
👉 Link: [Gmail-Hilfeseiten](https://support.google.com/mail/answer/185833?hl=de&ref_topic=3394217&sjid=4026180072124364108-EU)
- Andere Anbieter können unterschiedliche SMTP-Einstellungen erfordern
- Falsche Konfiguration führt dazu, dass die Zustellung der E-Mail fehlschlägt  
-> die Transkription wird trotzdem als `.txt`-Datei gespeichert.

---

### 3. Beispiel Workflow

```bash
./run.sh
```

**Ablauf:**

- Datei angeben oder Aufnahme starten
- Transkription durchführen
- Ergebnis speichern oder per Mail versenden (falls konfiguriert)

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

### 3. Projektdokumentation

Die vollständige Projektdokumentation, einschließlich **Installation**, Architektur und API-Referenz, ist auf GitHub Pages verfügbar:

👉 Link: https://onplastic.github.io/Audio_Transcription/

Die **README** dient als Einstiegspunkt – Details und Architektur sind in der Doku beschrieben.

---

### 5. Tests

Tests werden mit `pytest` ausgeführt:

```bash
PYTHONPATH=src pytest
```

**Aktueller Stand:**

- Basistests für Kernmodule vorhanden
- Fokus auf Eingabelogik, Output und Logging

---

### 6. Releases

Aktuelle Version: **v1.1.2**

Release enthält:

- CI Main Check (Release Gate)
- Docs Build Check (pdoc integration)
- Pages Deploy Prozess für die API Dokumentation
- Dokumentation des Automatisierungssystems (`automation.md`)

---

### ✏️ Autor

sIn OnPlastic

### ☕ Support

Wenn dir das Projekt gefällt und du es hilfreich findest, gib einen Kaffee aus:

> [![Ko-fi](https://img.shields.io/badge/-Ko--fi-ff5e5b?logo=ko-fi&logoColor=white)](https://ko-fi.com/onplastic)

Dankeschön 🙂
