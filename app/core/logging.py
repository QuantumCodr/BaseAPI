import logging
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)


class BaseAPIFormatter(logging.Formatter):

    def formatTime(self, record, datefmt=None):
        from datetime import datetime

        dt = datetime.fromtimestamp(record.created)

        # manually inject microseconds
        return dt.strftime("%Y-%m-%d %H:%M:%S") + f",{dt.microsecond:06d}"

    def format(self, record):
        msg = record.getMessage()

        # PHASE HEADER
        if msg.startswith("PHASE_HEADER::"):
            title = msg.replace("PHASE_HEADER::", "")
            return (
                "\n"
                + "=" * 60
                + f"\n{title}\n"
                + "=" * 60
            )

        # SECTION HEADER
        if msg.startswith("SECTION::"):
            title = msg.replace("SECTION::", "")
            return (
                "\n"
                + "-" * 60
                + f"\n{title}\n"
                + "-" * 60
            )

        time = self.formatTime(record)

        return f"[{time}] {record.levelname:<5} | {msg}"


logger = logging.getLogger("baseapi")
logger.setLevel(logging.INFO)
logger.propagate = False

if not logger.handlers:

    formatter = BaseAPIFormatter()

    file_handler = logging.FileHandler(
        LOG_DIR / "app.log",
        encoding="utf-8"
    )

    console_handler = logging.StreamHandler()

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


def phase(title: str):
    logger.info(f"PHASE_HEADER::PHASE : {title}")


def section(title: str):
    logger.info(f"SECTION::{title}")


def log(msg: str):
    logger.info(msg)