"""
Console utilities.

Every CLI command should use this module instead of
calling print() directly.
"""

import sys


def info(message: str):
    """
    General information.
    """
    print(message)


def success(message: str):
    """
    Successful operation.
    """
    print(f"✓ {message}")


def warning(message: str):
    """
    Warning message.
    """
    print(f"⚠ {message}")


def error(message: str):
    """
    Error message.
    """
    print(f"✗ {message}", file=sys.stderr)


def title(message: str):
    """
    Section heading.
    """
    print(f"\n=== {message} ===")


def divider():
    """
    Print a divider line.
    """
    print("-" * 50)