from __future__ import annotations
"""
logging_setup.py

Central logging configuration for the CLI application.

This module initializes the root logger and writes all log messages
to timestamped log file inside the configured log directory.
"""

import logging
from datetime import datetime
from pathlib import Path


def setup_logging(log_dir: Path, level: str = "INFO") -> Path:
    """
    **Initialize application logging.**

    The function creates the log directory if necessary, configures the
    root logger with the requested level, removes previously attached
    handlers, and installs a single file handler that writes to a
    timestamped log file.

    Parameters
    ----------
        log_dir : Path
            Directory where log files should be written.
        level : str, default="INFO"
            Logging level as a string ("DEBUG", "INFO").

    Returns
    -------
        Path
            Full path to the log file.
    """

    # --- Ensure log directory exists ---
    log_dir.mkdir(parents=True, exist_ok=True)
    logfile = log_dir / f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

    # --- Resolve configured logging level ---
    numeric_level = getattr(logging, level.upper(), logging.INFO)

    # --- Configure root logger ---
    root = logging.getLogger()
    root.setLevel(numeric_level)

    # --- Remove existing handlers to avoid duplicate logs --- 
    if root.handlers:
        root.handlers.clear()

    fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")

    # --- Write logs to file only ---    
    fh = logging.FileHandler(logfile, encoding="utf-8")
    fh.setLevel(numeric_level)
    fh.setFormatter(fmt)
    root.addHandler(fh)

    logging.getLogger(__name__).info("Logging initialized: %s", logfile)
    return logfile
