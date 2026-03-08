from __future__ import annotations
"""
main.py

Main CLI entry point for the audio Transcription tool.

Workflow:
---------
1. Load environment variables and runtime configuration.
2. Ask whether an audiofile already exists.
3. Either resolve the input audio path or switch to live recording.
4. Ask whether the result should only be saved or also sent by email.
5. Run Whisper transcription.
6. Save transcript to disk.
7. Optionally send the transcript by email.
"""

import logging
import os
from pathlib import Path

from dotenv import load_dotenv

from config import load_config
from input_utils import ask_choice, ask_email, ask_audio_path
from logging_setup import setup_logging
from mailer import SmtpSettings, send_mail_text
from output import write_txt
from paths import build_output_txt_path
from recorder import record_until_enter
from whisper_asr import transcribe_file

load_dotenv()


def main() -> int:
    """
    Run the CLI transcription workflow.

    Returns
    -------
    int
        Process exit code.
         
        0 Successful execution
        130 User aborted via (CTRL+C)
    """
    
    # --- Print CLI header ---
    title = "Audio_Transkription by sIn v0.2"
    print(f"\n{title}")
    print("=" * len(title))
    print("(CTRL+C) beendet das Programm\n")

    try:
        # --- Resolve project root and load configuration ---
        project_root = Path(__file__).resolve().parents[1]
        cfg = load_config(project_root)

        # --- Initialize logging ---
        setup_logging(cfg.log_dir, cfg.log_level)
        log = logging.getLogger(__name__)
        log.info("Audio_Transkription by sIn")

        output_dir = cfg.output_dir.resolve()

        # --- Ask whether an audio file already exists ---
        audio_vorhanden = ask_choice(
            "Audio-Datei vorhanden? ",
            {"j": True, "n": False}
        )

        audio_path: Path | None = None

        # --- Resolve input source: existing audio file or live recording ---
        if audio_vorhanden:
            audio_path = ask_audio_path(project_root)

            if audio_path is None:
                audio_vorhanden = False
                print("\n-> Die Audioaufnahme startet gleich automatisch...\n")
        else:
            print("\n-> Die Audioaufnahme startet gleich automatisch...\n")

        # --- Ask whether to save or send by email ---
        mode = ask_choice(
            "Ergebnis in .txt (s)peichern, oder zusätzlich E(m)ail versenden? ",
            {"s": "save", "m": "mail"},
        )

        # --- Ask for recipient address if mail delivery is requested ---
        to_addr: str | None = None
        if mode == "mail":
            to_addr = ask_email()

        # --- Record audio if no existing file is used ---
        if not audio_vorhanden:
            recordings_dir = project_root / "input" / "recordings"
            audio_path = record_until_enter(output_dir=recordings_dir)
            log.info("Recorded audio saved: %s", audio_path)
        
        # --- Type-Safety: audio_path must exist at this point ---
        if audio_path is None:
            raise RuntimeError("Audio path should not be None at this point.")

        # --- Run transcription ---
        log.info("Mode selected: %s", mode)
        print("\n-> Transkription startet...\n")
        txt = transcribe_file(
            audio_path,
            cfg.model_name,
            cfg.language,
        )

        # --- Write transcript to disk ---
        out_txt = build_output_txt_path(output_dir, audio_path)
        write_txt(out_txt, txt)
        log.info("Ergebnis gespeichert: %s", out_txt)

        print(f"Transkription gespeichert: {out_txt}\n")
        
        # --- Send transcript by email if requested ---
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

            print("Mail wurde gesendet.\n")

        print("-> Programm beendet!\n")
        return 0

    except KeyboardInterrupt:
        print("\nAbbruch durch Benutzer (CTRL+C)\n")
        log = logging.getLogger(__name__)
        log.info("Programm mit KeyboardInterrupt beendet.")
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
