
from pathlib import Path
import os
import tempfile


def validate_file_path(file_path):
    """Validate an absolute file path."""

    if not file_path or not str(file_path).strip():
        raise ValueError("File path cannot be empty.")

    path = Path(file_path).expanduser()

    if not path.is_absolute():
        raise ValueError("Please provide an absolute file path.")

    parent = path.parent.resolve(strict=True)

    if not parent.is_dir():
        raise ValueError("The selected directory does not exist.")

    if path.is_symlink():
        raise ValueError("Symbolic links are not supported.")

    return parent / path.name


def create_file(file_path):
    """Create a new empty text file."""

    path = validate_file_path(file_path)

    if path.exists():
        raise FileExistsError("File already exists.")

    if not path.name:
        raise ValueError("A valid filename is required.")

    path.touch(exist_ok=False)

    return path


def read_file(file_path):
    """Read the contents of an existing text file."""

    path = validate_file_path(file_path)

    if not path.exists():
        raise FileNotFoundError("File does not exist.")

    if not path.is_file():
        raise ValueError("Selected path is not a file.")

    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        raise ValueError("This file is not a UTF-8 text file.")


def save_file(file_path, content):
    """Save or update the contents of a text file."""

    path = validate_file_path(file_path)

    if path.exists() and not path.is_file():
        raise ValueError("Selected path is not a file.")

    if path.exists() and path.read_text(encoding="utf-8") == content:
        return False

    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        dir=path.parent,
        delete=False
    ) as temp_file:

        temp_file.write(content)
        temp_path = Path(temp_file.name)

    try:
        os.replace(temp_path, path)
    finally:
        if temp_path.exists():
            temp_path.unlink()

    return True


def create_folder(folder_path):
    """Create a new folder inside an existing directory."""

    if not folder_path or not str(folder_path).strip():
        raise ValueError("Folder path cannot be empty.")

    path = Path(folder_path).expanduser()

    if not path.is_absolute():
        raise ValueError("Please provide an absolute folder path.")

    parent = path.parent.resolve(strict=True)

    if not parent.is_dir():
        raise ValueError("Parent directory does not exist.")

    if path.is_symlink():
        raise ValueError("Symbolic links are not supported.")

    folder = parent / path.name

    if folder.exists():
        raise FileExistsError("Folder already exists.")

    folder.mkdir()

    return folder


def list_directory(directory_path):
    """Return the files and folders inside a directory."""

    if not directory_path or not str(directory_path).strip():
        raise ValueError("Directory path cannot be empty.")

    path = Path(directory_path).expanduser().resolve(strict=True)

    if not path.is_dir():
        raise ValueError("Selected path is not a directory.")

    items = []

    for item in sorted(path.iterdir(), key=lambda entry: (not entry.is_dir(), entry.name.lower())):

        if item.is_symlink():
            continue

        if item.is_dir():
            items.append({
                "name": item.name,
                "path": str(item),
                "type": "folder"
            })

        elif item.is_file():
            items.append({
                "name": item.name,
                "path": str(item),
                "type": "file"
            })

    return items
