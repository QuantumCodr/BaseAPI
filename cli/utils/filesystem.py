from pathlib import Path


def project_exists(project_name: str) -> bool:
    return Path(project_name).exists()


def resolve_project_path(project_name: str) -> Path:
    return Path.cwd() / project_name


def ensure_directory_available(project_name: str) -> Path:
    path = resolve_project_path(project_name)

    if path.exists():
        raise FileExistsError(
            f"Directory '{project_name}' already exists."
        )

    return path