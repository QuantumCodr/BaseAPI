from pathlib import Path

from cli.console import (
    success,
    title,
    info,
    error,
)

from cli.utils.filesystem import (
    ensure_directory_available,
)

from cli.utils.copier import copy_project
from cli.utils.renderer import render_directory
from cli.utils.manifest import create_manifest

from cli import __version__


def run_create(request):
    """
    BaseAPI project generator entry point
    """

    if not request.arguments:
        error("Project name required.")
        return

    project_name = request.arguments[0]

    title("BaseAPI Project Generator")

    info(f"Project: {project_name}")

    try:
        # =====================================================
        # 1. Resolve path
        # =====================================================
        destination = ensure_directory_available(project_name)

        # =====================================================
        # 2. Create empty directory
        # =====================================================
        destination.mkdir(parents=True, exist_ok=True)

        # =====================================================
        # 3. Copy FULL BaseAPI source (NOT templates)
        # =====================================================
        source = Path(__file__).resolve().parents[2]  # root project

        copy_project(source, destination)

        # =====================================================
        # 4. Render placeholders (branding / metadata)
        # =====================================================
        context = {
            "PROJECT_NAME": project_name,
            "BASEAPI_VERSION": __version__,
            "PACKAGE_NAME": project_name.replace("-", "_"),
            "YEAR": "2026",
        }

        render_directory(destination, context)

        # =====================================================
        # 5. Create manifest (for upgrade system)
        # =====================================================
        create_manifest(destination, __version__)

        # =====================================================
        # 6. Success output
        # =====================================================
        success("Project successfully created 🚀")

        info(f"Location: {destination}")
        info("")
        info("Next steps:")
        info(f"cd {project_name}")
        info("pip install -r requirements.txt")
        info("uvicorn app.main:app --reload")

    except FileExistsError:
        error("Project already exists.")

    except Exception as e:
        error(f"Failed to create project: {e}")