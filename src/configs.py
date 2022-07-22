import logging
from logging.handlers import RotatingFileHandler

from constants import LOG_DIR, LOG_FILE, LOG_FORMAT


def configure_logging():
    """Конфигурация логгера.
    """
    LOG_DIR.mkdir(exist_ok=True)

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = RotatingFileHandler(
        filename=LOG_FILE,
        maxBytes=10 ** 6,
        backupCount=3,
        encoding='utf-8'
    )
    formatter = logging.Formatter(LOG_FORMAT)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
