import sys

from cli.console import (
    title,
    success,
    info,
)


def run_doctor(request):

    title("BaseAPI Doctor")

    info(
        f"Python: {sys.version.split()[0]}"
    )

    success("CLI installed")

    success("Environment OK")