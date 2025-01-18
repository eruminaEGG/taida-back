import logging


def get_logger() -> logging.Logger:
    logger: logging.Logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    return logger
