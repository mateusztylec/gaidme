import os
import logging
from colorlog import ColoredFormatter

def get_logger(logger_name):
    log_level = os.getenv("GAIDME_LOG_LEVEL", "WARNING").upper()
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)
    logger.propagate = False  # Prevent log propagation to avoid double logging

    # Define formatters
    date_format = "%d-%m %H:%M:%S"

    color_formatter = ColoredFormatter(
        "%(log_color)s[%(levelname)s]%(reset)s %(name)s [%(filename)s:%(lineno)d]: %(message)s",
        datefmt=date_format,
        log_colors={
            "DEBUG":    "cyan",
            "INFO":     "green",
            "WARNING":  "yellow",
            "ERROR":    "red",
            "CRITICAL": "bold_red",
        },
        reset=True,
        style="%"
    )

    # Create console handler with color support
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(color_formatter)

    # Add handlers if they are not already added
    if not logger.handlers:
        logger.addHandler(console_handler)

    return logger