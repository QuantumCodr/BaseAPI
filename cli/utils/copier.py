import shutil
from pathlib import Path


def copy_directory(source: Path, destination: Path):
    """
    Copy an entire directory.
    """
    shutil.copytree(source, destination)