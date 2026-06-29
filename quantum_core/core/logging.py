import logging
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

logger = logging.getLogger("quantum_core")

logger.setLevel(logging.INFO)

logger.propagate = False

file_handler = logging.FileHandler(
    LOG_DIR / "app.log",
    encoding="utf-8"
)

formatter = logging.Formatter(
    """
=============================
TIME: %(asctime)s
LEVEL: %(levelname)s
MESSAGE: %(message)s
=============================
"""
)

file_handler.setFormatter(formatter)

logger.handlers.clear()

logger.addHandler(file_handler)