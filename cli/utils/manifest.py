import json
from pathlib import Path
from datetime import datetime

BASEAPI_DIR = ".baseapi"


def get_manifest_dir(project_path: Path) -> Path:
    return project_path / BASEAPI_DIR


def ensure_manifest_dir(project_path: Path) -> Path:
    path = get_manifest_dir(project_path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def create_manifest(project_path: Path, version: str):
    """
    Create BaseAPI manifest.json inside generated project.
    """

    manifest_dir = ensure_manifest_dir(project_path)

    manifest = {
        "project": project_path.name,
        "baseapi_version": version,
        "created_at": datetime.utcnow().isoformat(),
        "modules": [],
    }

    file_path = manifest_dir / "manifest.json"

    file_path.write_text(json.dumps(manifest, indent=4))

    return file_path


def load_manifest(project_path: Path):
    """
    Load existing manifest.
    """

    file_path = get_manifest_dir(project_path) / "manifest.json"

    if not file_path.exists():
        return None

    return json.loads(file_path.read_text())


def update_manifest(project_path: Path, data: dict):
    """
    Update manifest safely.
    """

    file_path = get_manifest_dir(project_path) / "manifest.json"

    if not file_path.exists():
        raise FileNotFoundError("Manifest not found")

    current = json.loads(file_path.read_text())

    current.update(data)

    file_path.write_text(json.dumps(current, indent=4))

    return current