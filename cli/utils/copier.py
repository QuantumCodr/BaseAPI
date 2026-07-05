from pathlib import Path
import shutil

from cli.utils.ignore import (
    load_ignore_patterns,
    should_ignore,
)


def copy_project(source: Path, destination: Path):
    """
    Copy BaseAPI source into a new project directory
    while respecting .cliignore rules.
    """

    patterns = load_ignore_patterns(source)

    for item in source.rglob("*"):

        relative_path = item.relative_to(source)

        # Check ignore rules
        if should_ignore(relative_path, patterns):
            continue

        target_path = destination / relative_path

        # Directory
        if item.is_dir():
            target_path.mkdir(parents=True, exist_ok=True)
            continue

        # File
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(item, target_path)