from pathlib import Path


# =====================================================
# SUPPORTED TEXT FILES
# =====================================================

TEXT_FILE_EXTENSIONS = {
    ".py",
    ".md",
    ".txt",
    ".toml",
    ".json",
    ".yaml",
    ".yml",
    ".ini",
    ".env",
    ".html",
    ".css",
    ".js",
    ".ts",
}


# =====================================================
# HELPERS
# =====================================================

def is_text_file(file_path: Path) -> bool:
    """
    Returns True if the file should be rendered.
    """

    return file_path.suffix.lower() in TEXT_FILE_EXTENSIONS


def render_file(file_path: Path, context: dict):
    """
    Replace placeholders inside a single file.
    """

    if not is_text_file(file_path):
        return

    content = file_path.read_text(encoding="utf-8")

    for key, value in context.items():

        placeholder = "{{" + key + "}}"

        content = content.replace(
            placeholder,
            str(value)
        )

    file_path.write_text(
        content,
        encoding="utf-8"
    )


# =====================================================
# PUBLIC API
# =====================================================

def render_directory(directory: Path, context: dict):
    """
    Render every supported file in a project.
    """

    for file_path in directory.rglob("*"):

        if file_path.is_file():

            render_file(
                file_path,
                context
            )