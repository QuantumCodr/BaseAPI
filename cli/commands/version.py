from cli import __version__
from cli.console import info


def run_version(request):

    info(
        f"BaseAPI CLI v{__version__}"
    )