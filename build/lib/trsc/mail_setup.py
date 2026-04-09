"""
mail_setup.py

CLI setup tool for mail configuration.

Responsibilities
----------------
- Ask the user for mail-related configuration values
- Optionally test SMTP connection and login credentials
- Write mail settings to config.toml
- Write mail secrets to the .env file

Notes
-----
The mail feature is optional.

This setup tool allows users to configure SMTP settings interactively
and optionally verify the configuration before saving.

No email is sent during the configuration test.
"""

from __future__ import annotations

import logging
from pathlib import Path

from .system_checks import ensure_valid_working_directory
from .config import load_config
from .input_utils import ask_choice, ask_port, prompt_input
from .logging_setup import setup_logging
from .mail_config import (
    test_mail_connection,
    update_mail_config, 
    write_mail_env,
)
from .version import __version__

SETUP_NAME = "Mail_Konfiguration by sIn"


def main() -> int:
    """
    **Run the mail configuration setup workflow.**

    Workflow
    --------
    1. Show the CLI setup header.
    2. Resolve and validate the TRSC working directory.
    3. Ask the user for mail-related configuration values.
    4. Optionally test the SMTP connection and login.
    5. Ask whether the values should be saved.
    6. Write config.toml and .env if confirmed.

    The configuration test only checks connection and authentication.
    No email is sent during process.

    Returns
    -------
        int
            Process exit code:
            - (0) Successful execution
            - (130) User aborted via (CTRL+C)
    
    """

    # --- Print CLI Header ---
    title = f"{SETUP_NAME} v{__version__}"
    print(f"\n{title}")
    print("=" * len(title))
    print("(CTRL+C) beendet das Programm\n")

    try:
        # --- Resolve TRSC working directory ---
        project_root = Path.cwd()

        # --- Validate TRSC working directory structure ---
        ensure_valid_working_directory(project_root)

        # --- Initialize config paths ---
        config_path = project_root / "config.toml"
        env_path = project_root / ".env"

        # --- Initialize logging ---
        cfg = load_config(project_root)
        setup_logging(cfg.log_dir, cfg.log_level)
        log = logging.getLogger(__name__)
        log.info("Mail setup v%s started", __version__)

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

        # --- Optionally test SMTP connection before saving ---
        test_config = ask_choice(
            "Konfiguration testen?",
            {"j": True, "n": False},
        )

        print()

        if test_config:
            connection_ok = test_mail_connection(
                smtp_host=smtp_host,
                smtp_port=smtp_port,
                smtp_use_ssl=smtp_use_ssl,
                smtp_user=smtp_user,
                smtp_app_password=smtp_app_password,
            )

            if connection_ok:
                log.info("SMTP setup successful.")
                print("Verbindung erfolgreich.\n")
            
            else:
                log.info("SMTP setup failed.")
                print("Verbindungsaufbau fehlgeschlagen.\n")

                retry_setup = ask_choice(
                    "Eingaben bearbeiten?",
                    {"j": True, "n": False},
                )

                print()

                if retry_setup:
                    log.info("Mail setup tool restarted by user")
                    return main()

        # --- Confirm whether the configuration should be saved ---
        save_values = ask_choice(
            "Sollen die Eingaben gespeichert werden?",
            {"j": True, "n": False},
        )

        # --- Abort setup without saving changes ---
        if not save_values:
            log.info("Mail setup aborted. No values saved.")
            print("\nEingaben wurden nicht gespeichert.\n")
            return 0

        # --- Update config.toml with mail settings ---
        log.info("Mail setup approved. Values are saved.")
        update_mail_config(
            config_path=config_path,
            smtp_host=smtp_host,
            smtp_port=smtp_port,
            smtp_use_ssl=smtp_use_ssl,
            from_name=from_name,
            subject_prefix=subject_prefix,
        )
        log.info("Values saved in file config.toml: %s", config_path)

        # --- Write mail secrets to .env ---
        write_mail_env(
            env_path=env_path,
            smtp_user=smtp_user,
            smtp_app_password=smtp_app_password,
        )
        log.info("Mail-secrets saved in file .env: %s", env_path)

        # --- Setup completed successfully ---
        log.info("Mail setup successful.")
        print("\nMail-Konfiguration wurde gespeichert.\n")
        return 0

    # --- Handle user abort (CTRL+C) ---
    except KeyboardInterrupt:
        print("\nAbbruch durch Benutzer (CTRL+C)\n")
        log = logging.getLogger(__name__)
        log.info("Mail setup canceled by user.")
        return 130

if __name__ == "__main__":
    raise SystemExit(main())

