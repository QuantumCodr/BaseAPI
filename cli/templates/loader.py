from pathlib import Path
from cli.utils.copier import copy_directory


def get_project_template():
    """
    Returns the base project template path.
    """
    return Path(__file__).parent / "project" / "baseapi"


def load_project_template(destination: Path):
    """
    Copies BaseAPI starter template into target project.
    """
    template_path = get_project_template()

    if not template_path.exists():
        raise FileNotFoundError("BaseAPI template not found")

    copy_directory(template_path, destination)