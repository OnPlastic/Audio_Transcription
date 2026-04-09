"""
init_setup.py

CLI setup tool for initializing a TRSC working directory.

Responsibilities
----------------
- Ask the user where the TRSC structure should be created
- Resolve and preview the selected target directory
- Show the planned TRSC directory structure
- Detect whether config.toml already exists
- Create the required TRSC directory structure
- Write a default config.toml if needed

Notes
-----
This setup tool initializes a valid TRSC working directory structure
for the installable CLI workflow.

The mail configuration is intentionally not part of this setup.
It can be added later via the dedicated mail setup tool.
"""

from __future__ import annotations

from pathlib import Path

from .input_utils import ask_choice, prompt_input
from .version import __version__

SETUP_NAME = "TRSC_Init by sIn"


def build_default_config_text() -> str:
    """
    **Build the default config.toml content for a new TRSC setup.**

    Returns
    -------
        str
            Default TOML content for config.toml.
    """

    return """[transcription]
model_name = "large-v3"
language = "de"
output_dir = "output"

[logging]
log_dir = "logs"
log_level = "INFO"
"""


def create_trsc_directories(target_dir: Path) -> None:
    """
    **Create the required TRSC directory structure.**

    Parameters
    ----------
        target_dir : Path
            Base directory where the TRSC structure should be created.
    """

    (target_dir / "input").mkdir(parents=True, exist_ok=True)
    (target_dir / "input" / "audio").mkdir(parents=True, exist_ok=True)
    (target_dir / "input" / "recordings").mkdir(parents=True, exist_ok=True)
    (target_dir / "output").mkdir(parents=True, exist_ok=True)
    (target_dir / "logs").mkdir(parents=True, exist_ok=True)


def write_config_if_needed(config_path: Path, overwrite_config: bool) -> bool:
    """
    **Write config.toml if it does not exist or if overwrite was approved.**

    Parameters
    ----------
        config_path : Path
            Path to the config.toml file.
        overwrite_config : bool
            Whether an existing config.toml may be overwritten.
    
    Returns
    -------
        bool
            True if config.toml was written, otherwise False.
    """

    if config_path.exists() and not overwrite_config:
        return False
    
    config_path.write_text(build_default_config_text(), encoding="utf-8")
    return True


def main() -> int:
    """
    **Start the TRSC initialization setup CLI workflow.**

    Workflow
    --------
    1. Show the CLI setup header.
    2. Ask whether the TRSC structure should be created 
       in the current directory or at a user-defined path.
    3. Resolve the target directory.
    4. Show the target directory and the planned structure.
    5. Check whether config.toml already exists.
    6. Ask for final confirmation.
    7. Create the TRSC directory structure.
    8. Write config.toml if needed.

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
            "TRSC-Struktur (h)ier erstellen oder (p)fad angeben?",
            {"h": "here", "p": "path"},
        )

        print()

        # --- Resolve the target directory ---
        if target_mode == "here":
            target_dir = Path.cwd().resolve()
        else:
            raw_path = prompt_input(
                "Bitte Zielpfad eingeben "
                "(z.B. ~/trsc-projekt): "    
            )
            target_dir = Path(raw_path).expanduser().resolve()

        # --- Check whether config.toml already exists in target directory ---
        config_path = target_dir / "config.toml"
        config_exists = config_path.exists()

        # --- Show target directory and planned structure ---
        print()
        print(f"Zielverzeichnis: {target_dir}\n")

        print("Folgende Struktur wird erstellt:")
        print("- config.toml")
        print("- input/audio/")
        print("- input/recordings/")
        print("- output/")
        print("- logs/\n")

        overwrite_config: bool = False

        if config_exists:
            print("Hinweis: config.toml existiert bereits.\n")

            overwrite_config = bool(ask_choice(
                "config.toml überschreiben?",
                {"j": True, "n": False}
            ))

            print()
    
        # --- Ask for final confirmation before creating the structure ---
        save_structure = ask_choice(
            "Soll die TRSC-Struktur erstellt werden?",
            {"j": True, "n": False},
        )

        print()

        if not save_structure:
            print("TRSC-Struktur wurde nicht erstellt.\n")
            return 0
        
        # --- Ensure target directory exists ---
        target_dir.mkdir(parents=True, exist_ok=True)

        # --- Create TRSC directory structure ---
        create_trsc_directories(target_dir)

        # --- Write config.toml if needed ---
        config_written = write_config_if_needed(
            config_path=config_path,
            overwrite_config=overwrite_config,
        )

        # --- Print result ---
        print("TRSC-Struktur wurde erstellt.\n")

        if config_written:
            print("config.toml wurde geschrieben.\n")
        else:
            print("Vorhandene config.toml wurde beibehalten.\n")
        
        print("Nächste Schritte:")
        print(f" - In das Zielverzeichnis wechseln: cd {target_dir}")
        print(" - Tool starten mit: trsc\n")
        print("[Optional:]")
        print("- Mail einrichten mit: trsc-mail-setup\n")
        
        return 0
    
    # --- Handle user abort (CTRL+C) ---
    except KeyboardInterrupt:
        print("\nAbbruch durch Benutzer (CTRL+C)\n")
        return 130
    
if __name__ == "__main__":
    raise SystemExit(main())