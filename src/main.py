from __future__ import annotations

import os
import logging
from pathlib import Path

from dotenv import load_dotenv

from logging_setup import setup_logging
from config import load_config
from paths import build_output_txt_path
from output import write_txt
from whisper_asr import transcribe_file
from mailer import SmtpSettings, send_mail_text
from recorder import record_until_enter
from input_utils import ask_choice, ask_email, ask_audio_path


load_dotenv()


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
        audio_vorhanden = ask_choice(
            "Audio-Datei vorhanden? ",
            {"j": True, "n": False}
        )

        audio_path: Path | None = None

        if audio_vorhanden:
            audio_path = ask_audio_path(project_root)

            if audio_path is None:
                audio_vorhanden = False
                print("\n-> Die Audioaufnahme startet gleich automatisch...\n")
        else:
            print("\n-> Die Audioaufnahme startet gleich automatisch...\n")

        # ---2. Abfrage ---
        mode = ask_choice(
            "Ergebnis in .txt speichern(s), oder zusätzlich Mail(m) versenden? ",
            {"s": "save", "m": "mail"},
        )

        # --- 3. Abfrage (nur bei Mail) ---
        to_addr: str | None = None
        if mode == "mail":
            to_addr = ask_email()

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
        if mode == "mail":
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
