import logging
from logging.handlers import RotatingFileHandler
import sys


def setup_logging(log_file: str = "app.log", level: int = logging.DEBUG) -> None:
    root = logging.getLogger()
    if root.handlers:
        return

    root.setLevel(level)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    file_handler = RotatingFileHandler(log_file, maxBytes=100 * 1024 * 1024, backupCount=1)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(level)
    root.addHandler(file_handler)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level)
    root.addHandler(console_handler)


