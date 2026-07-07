from importlib.metadata import version
from pathlib import Path
import platform
import sys


def register(subparsers):
    parser = subparsers.add_parser(
        "version",
        help="Show BaseAPI version information",
    )

    parser.set_defaults(handler=run)


def run(args):
    baseapi_version = version("baseapi")

    print(
f"""
==========================================
              BaseAPI
==========================================

Version     : {baseapi_version}

Python      : {platform.python_version()}
Platform    : {platform.system()}
Location    : {Path.cwd()}

Status      : Ready

==========================================
"""
    )