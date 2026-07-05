import logging
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

logger = logging.getLogger("baseapi")

logger.setLevel(logging.INFO)
logger.propagate = False

if not logger.handlers:

    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s | %(message)s"
    )

    file_handler = logging.FileHandler(
        LOG_DIR / "app.log",
        encoding="utf-8"
    )

    console_handler = logging.StreamHandler()

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)