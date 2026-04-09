"""
init_setup.py

CLI setup tool for initializing a TRSC working directory.

Responsibilities
----------------
- Ask the user where the TRSC structure should be created
- Show a preview of the target directory
- Prepare the initialization workflow for later file creation

Notes
-----
This setup tool does not yet write any files in the first minimal version.

It is intended to initialize a valid TRSC working directory structure
for the installable CLI workflow.
"""

from __future__ import annotations

from pathlib import Path

from trsc.input_utils import ask_choice, prompt_input
from trsc.version import APP_NAME, __version__

SETUP_NAME = "TRSC_Init_Tool by sIn"


def main() -> int:
    """
    **Start the TRSC initialization setup CLI workflow.**

    Workflow
    --------
    1. Show the ClI setup Header.
    2. Ask whether the TRSC structure should be created here
       or at a user-defined path.
    3. Resolve the target directory.
    4. Show the resolved target directory.

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
        # --- Ask where the TRSC structure should be created ---
        target_mode = ask_choice(
            "TRSC-Struktur (h)ier erstellen, oder (P)fad angeben?",
            {"h": "here", "P": "path"},
        )

        print()

        # --- Resolve the directory ---
        if target_mode == "here":
            target_dir = Path.cwd()
        else:
            raw_path = prompt_input("Bitte Zielpfad eingeben: ")
            target_dir = Path(raw_path).expanduser().resolve()

        # --- Show resolved target directory ---
        print()
        print((f"Zielverzeichnis: {target_dir}\n"))

        print("Folgende Struktur wird erstellt:")
        print("- config.toml")
        print("- input/audio/")
        print("- input/recordings/")
        print("- output/")
        print("- logs/\n")

        return 0
    
    # --- Handle user abort (CTRl+C) ---
    except KeyboardInterrupt:
        print("\nAbbruch durch Benutzer. Programm Ende\n")
        return 130
    
if __name__ == "__main__":
    raise SystemExit(main())