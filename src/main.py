from __future__ import annotations

import os
import logging
from pathlib import Path

from dotenv import load_dotenv

from logging_setup import setup_logging
from config import load_config
from paths import normalize_input_path, build_output_txt_path
from output import write_txt
from whisper_asr import transcribe_file
from mailer import SmtpSettings, send_mail_text
from recorder import record_until_enter


load_dotenv()


def ask_yes_no(prompt: str) -> bool:
    while True:
        ans = input(prompt).strip().lower()
        if ans in ("j", "ja", "y", "yes"):
            return True
        if ans in ("n", "nein", "no"):
            return False
        print("Bitte J/N eingeben.")


def ask_choice(prompt: str, choices: tuple[str, ...]) -> str:
    while True:
        ans = input(prompt).strip().upper()
        if ans in choices:
            return ans
        print(f"Bitte {'/'.join(choices)} eingeben.")


def main() -> int:
    
    print("\n----- Spracherkennung by sIn -----")
    print(":~/.. -> Programmende mit (CTRL+C)\n")

    try:

        project_root = Path(__file__).resolve().parents[1]
        cfg = load_config(project_root)

        setup_logging(cfg.log_dir, cfg.log_level)
        log = logging.getLogger(__name__)
        log.info("Start Spracherkennung by sIn")

        output_dir = cfg.output_dir.resolve()

        # --- 1. Abfrage ---
        audio_vorhanden = ask_yes_no("Audio vorhanden? (J/N): ")

        audio_path: Path | None = None

        if audio_vorhanden:

            # --- Default: input/audio (für Handy-Upload via scp) ---
            default_audio_dir = project_root / "input" / "audio"

            while True:
                raw = input("Bitte Dateiname oder Pfad zur Audio-Datei angeben: ").strip()

                # --- Wenn nur Dateiname, dann im default_audio_dir suchen ---
                if raw and ("/" not in raw) and ("\\" not in raw) and (not raw.startswith("~")):
                    audio_path = (default_audio_dir / raw).resolve()
                else:
                    audio_path = normalize_input_path(raw)

                if audio_path.exists():
                    print("Datei gewählt:", audio_path)
                    break

                print("Datei nicht gefunden:", audio_path)
                if ask_yes_no("Nochmal versuchen? (J/N): "):
                    continue

                action = ask_choice(
                    "Programm beenden (B) oder Audio aufnehmen (A)? ",
                    ("B", "A")
                )

                if action == "B":
                    return 2
                
                # --- action == "A" -> Wechsel in den Recorder-Pfad, nach der Mode-Abfrage ---
                audio_vorhanden = False
                audio_path = None
                print("Recorder startet automatisch nach der nächsten Abfrage.")
                break

        else:
            print("Recorder startet automatisch nach der nächsten Abfrage.")

        # ---2. Abfrage ---
        mode = ask_choice(
            "Ergebnis in .txt speichern (S), oder Mail senden (M)? ",
            ("S", "M"),
        )

        # --- 3. Abfrage (nur bei Mail) ---
        to_addr: str | None = None
        if mode == "M":
            while True:
                to_addr = input("Bitte Mailadresse eingeben: ").strip()

                if "@" in to_addr and "." in to_addr:
                    print("Mailadresse:", to_addr)
                    break
                print("Ungültige Mailadresse!!! Bitte erneut eingeben.")

        # --- Recorder nach der 3. Abfrage ---
        if not audio_vorhanden:
            recordings_dir = project_root / "input" / "recordings"
            audio_path = record_until_enter(output_dir=recordings_dir)
            log.info("Recorded audio saved: %s", audio_path)
        
        # --- Type-Safety: audio_path muss jetzt gesetzt sein ---
        if audio_path is None:
            raise RuntimeError("Audio path should not be None at this point.")

        # --- Transkription ---
        log.info("Mode selected: %s", mode)
        print("\nTranskription startet...\n")
        txt = transcribe_file(
            audio_path,
            cfg.model_name,
            cfg.language,
        )

        # --- Datei speichern ---
        out_txt = build_output_txt_path(output_dir, audio_path)
        write_txt(out_txt, txt)
        log.info("Ergebnis gespeichert: %s", out_txt)

        print("\nGespeichert:", out_txt)

        # --- Mailversand ---
        if mode == "M":
            log.info("Mail requested to: %s", to_addr)

            smtp = SmtpSettings(
                host=cfg.smtp_host,
                port=cfg.smtp_port,
                use_ssl=cfg.smtp_use_ssl,
                user=os.environ["SMTP_USER"],
                app_password=os.environ["SMTP_APP_PASSWORD"],
                from_name=cfg.from_name,
            )

            subject = f"{cfg.subject_prefix} {out_txt.stem}"

            if to_addr is None or not to_addr.strip():
                raise RuntimeError("to_addr should not be None when mode is M.")
            to_addr = to_addr.strip()

            send_mail_text(
                smtp=smtp,
                to_addr=to_addr,
                subject=subject,
                text_content=txt,
            )

            print("Mail wurde gesendet.")

        return 0

    except KeyboardInterrupt:
        print("\nAbbruch durch Benutzer. (CTRL+C)")
        log = logging.getLogger(__name__)
        log.info("Programm mit KeyboardInterrupt beendet.")
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
