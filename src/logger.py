import logging
from logging.handlers import TimedRotatingFileHandler
import logging.config
from src.constants import ROOT_DIR
import sys
from os.path import join


# Logging Levels
# https://docs.python.org/3/library/logger.html#logging-levels
# CRITICAL  50
# ERROR 40
# WARNING   30
# INFO  20
# DEBUG 10
# NOTSET    0

FORMATTER = logging.Formatter(f"[dev] "
                              f"[%(levelname)s]: [%(asctime)s] [%(lineno)d] [%(filename)s] [%(message)s]")
LOG_FILE = join(ROOT_DIR, "logs", "sadhuTrade.log")


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    console_handler.setLevel(logging.INFO)
    return console_handler


def get_file_handler():
    file_handler = TimedRotatingFileHandler(LOG_FILE)
    file_handler.setFormatter(FORMATTER)
    file_handler.setLevel(logging.DEBUG)
    return file_handler


def set_up_logging():
    logger = logging.getLogger(__name__)
    if not logger.hasHandlers():
        logger.setLevel(logging.DEBUG)
        logger.addHandler(get_console_handler())
        logger.addHandler(get_file_handler())
        logger.propagate = False

    return logger


if __name__ == "__main__":
    print(set_up_logging())
