from cli.console import (
    success,
    title,
    info,
    error,
)

from cli.utils.filesystem import (
    ensure_directory_available,
)

from cli.templates.loader import load_project_template
from pathlib import Path


def run_create(request):
    if not request.arguments:
        error("Project name required.")
        return

    project_name = request.arguments[0]

    title("BaseAPI Project Generator")

    info(f"Project: {project_name}")

    try:
        # 1. Get safe path
        destination = ensure_directory_available(project_name)

        # 3. Generate project from template
        load_project_template(destination)

        # 4. Success output
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