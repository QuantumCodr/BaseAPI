from pathlib import Path


DEFAULT_IGNORE_FILE = ".cliignore"


def load_ignore_patterns(root: Path):
    """
    Load ignore rules from .cliignore
    """

    ignore_file = root / DEFAULT_IGNORE_FILE

    if not ignore_file.exists():
        return []

    patterns = []

    for line in ignore_file.read_text().splitlines():

        line = line.strip()

        if not line:
            continue

        if line.startswith("#"):
            continue

        patterns.append(line)

    return patterns


def should_ignore(relative_path: Path, patterns):
    """
    Check if a file/folder should be ignored
    """

    path_str = relative_path.as_posix()

    for pattern in patterns:

        pattern = pattern.rstrip("/")

        # folder match
        if path_str.startswith(pattern):
            return True

        # exact file match
        if path_str == pattern:
            return True

    return False