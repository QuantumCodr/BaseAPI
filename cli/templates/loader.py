from pathlib import Path
from cli.utils.copier import copy_directory


def get_project_template():
    """
    Returns the base project template path.
    """
    return Path(__file__).parent / "project" / "default"


def load_project_template(destination: Path):

    template_path = get_project_template()

    print("TEMPLATE PATH:", template_path)
    print("EXISTS:", template_path.exists())
    print("FILES:", list(template_path.rglob("*")))

    if not template_path.exists():
        raise FileNotFoundError("BaseAPI template not found")

    copy_directory(template_path, destination)