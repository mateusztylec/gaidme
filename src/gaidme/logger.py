import os
import logging
from colorlog import ColoredFormatter
from logging.handlers import RotatingFileHandler

log_file = os.getenv("GAIDME_LOG_FILE_PATH", "app.log")

def get_logger(logger_name, log_file=log_file):
    log_level = os.getenv("LOG_LEVEL", "WARNING").upper()
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)
    logger.propagate = False  # Prevent log propagation to avoid double logging

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s [%(filename)s:%(lineno)d]: %(message)s",
        datefmt="%d-%m %H:%M:%S"
    )

    color_formatter = ColoredFormatter(
        "%(log_color)s[%(levelname)s]%(reset)s %(name)s [%(filename)s:%(lineno)d]: %(message)s",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red,bg_white",
        },
        reset=True,
        style="%",
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(color_formatter)

    # file_handler = RotatingFileHandler(
    #     log_file, maxBytes=5000000, backupCount=5
    # )  # 5MB file
    # file_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(console_handler)
        # logger.addHandler(file_handler)

    return logger