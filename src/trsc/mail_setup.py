"""
mail_setup.py

CLI setup tool for mail configuration.

Responsibilities
----------------
- Ask the user for mail-related configuration values
- Write mail settings to config.toml
- Write mail secrets to the .env file
"""

from __future__ import annotations

import logging
from pathlib import Path

from .config import load_config
from .input_utils import ask_choice, ask_port, prompt_input
from .logging_setup import setup_logging
from .mail_config import update_mail_config, write_mail_env
from .version import __version__

SETUP_NAME = "Mail_Konfiguration by sIn"

def main() -> int:
    """
    **Run the mail configuration setup workflow.

    Workflow
    --------
    1. Show the ClI setup header.
    2. Resolve the project root and config paths.
    3. Ask the user for mail-related configuration values.
    4. Ask whether the values should be saved.
    5. Write config.toml and .env if confirmed.

    Returns
    -------
        int
            Process exit code:
            - (0) Successful execution
            - (130) User aborted via (CTRL+C)
    """
    title = f"{SETUP_NAME} v{__version__}"
    print(f"\n{title}")
    print("=" * len(title))
    print("(CTRL+C) beendet das Programm\n")

    try:
        # --- Resolve project root and configuration paths ---
        project_root = Path(__file__).resolve().parents[2]
        config_path = project_root / "config.toml"
        env_path = project_root / ".env"

        # --- Initialize logging ---
        cfg = load_config(project_root)
        setup_logging(cfg.log_dir, cfg.log_level)
        log = logging.getLogger(__name__)
        log.info("Mail setup v%s gestartet", __version__)

        # --- Ask for mail configuration values ---
        smtp_host = prompt_input(
            "Bitte SMTP-Mailprovider eintragen "
            "(z.B. smtp.gmail.com): "
        )

        print()

        smtp_port = ask_port()

        print()

        smtp_use_ssl = bool(ask_choice(
            "SSL-Verschlüsselung verwenden?",
            {"j": True, "n": False},
        ))

        print()

        from_name = prompt_input(
            "Bitte Absendername eingeben "
            "(z.B. Audio_Transkription by sIn): "
        )

        print()

        subject_prefix = prompt_input(
            "Bitte Betreff-Präfix eingeben "
            "(z.B. [Transkript]): "
        )

        print()

        smtp_user = prompt_input(
            "Bitte SMTP-Usernamen eingeben "
            "(z.B. name@gmail.com):"
        )

        print()

        smtp_app_password = prompt_input(
            "Bitte SMTP-App-Passwort eingeben: "
        )

        print()

        # --- Confirm whether the configuration should be saved ---
        save_values = ask_choice(
            "Sollen die Eingaben gespeichert werden?",
            {"j": True, "n": False},
        )

        # --- Abort setup without saving changes ---
        if not save_values:
            log.info("Mail setup verworfen. Keine Werte gespeichert.")
            print("\nEingaben wurden nicht gespeichert.\n")
            return 0

        # --- Update config.toml with mail settings ---
        log.info("Mail Setup bestätigt. Werte werden aktualisiert.")
        update_mail_config(
            config_path=config_path,
            smtp_host=smtp_host,
            smtp_port=smtp_port,
            smtp_use_ssl=smtp_use_ssl,
            from_name=from_name,
            subject_prefix=subject_prefix,
        )
        log.info("Werte in config.toml aktualisiert: %s", config_path)

        # --- Write mail secrets to .env ---
        write_mail_env(
            env_path=env_path,
            smtp_user=smtp_user,
            smtp_app_password=smtp_app_password,
        )
        log.info("Mail-secrets in .env geschrieben: %s", env_path)

        # --- Setup completed successfully ---
        log.info("Mail setup erfolgreich abgeschlossen.")
        print("\nMail-Konfiguration wurde gespeichert.\n")
        return 0

    # --- Handle user abort (CTRL+C) ---
    except KeyboardInterrupt:
        print("\nAbbruch durch Benutzer (CTRL+C)\n")
        log = logging.getLogger(__name__)
        log.info("Mail setup durch Benutzer abgebrochen.")
        return 130

if __name__ == "__main__":
    raise SystemExit(main())

