import logging
import os

log_level = os.environ.get("GAIDME_LOG", "").upper()

log_level = "INFO" if log_level != "DEBUG" else "DEBUG"

def setup_logging() -> None:
    backend_logger = logging.getLogger("gaidme")
    backend_logger.setLevel(log_level)

    handler = logging.StreamHandler()
    handler.setLevel(log_level)

    formatter = logging.Formatter('%(levelname)s: %(name)s: %(message)s')
    handler.setFormatter(formatter)

    backend_logger.addHandler(handler)