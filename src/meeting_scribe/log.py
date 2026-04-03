"""Structured logging to stderr."""

import logging
import os
import sys


def get_logger(name: str) -> logging.Logger:
    """Get a logger that writes to stderr with a consistent format."""
    logger = logging.getLogger(f"meeting_scribe.{name}")

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stderr)
        handler.setFormatter(
            logging.Formatter("%(asctime)s [%(name)s] %(levelname)s — %(message)s", datefmt="%H:%M:%S")
        )
        logger.addHandler(handler)

    level = os.environ.get("LOG_LEVEL", "INFO").upper()
    logger.setLevel(getattr(logging, level, logging.INFO))

    return logger
