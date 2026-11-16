
import subprocess
from pathlib import Path


def run_git_command(command, directory):
    """
    Execute a Git command in the specified directory.
    """

    result = subprocess.run(
        command,
        cwd=directory,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(
            result.stderr.strip() or "Git command failed."
        )

    return result.stdout.strip()


def initialize_repository(directory):
    """
    Initialize a Git repository if one does not exist.
    """

    directory = Path(directory).resolve()

    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=directory,
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        return Path(result.stdout.strip())

    run_git_command(["git", "init"], directory)

    return directory


def commit_file(file_path, message=None):
    """
    Stage and commit a specific file.
    """

    file_path = Path(file_path).resolve()

    if not file_path.exists() or not file_path.is_file():
        raise FileNotFoundError("File does not exist.")

    repository = initialize_repository(file_path.parent)

    relative_path = file_path.relative_to(repository)

    if message is None:
        message = f"Updated {file_path.name}"

    run_git_command(
        ["git", "add", "--", str(relative_path)],
        repository
    )

    result = subprocess.run(
        ["git", "-c", "user.name=Notepad Tracker",
            "-c", "user.email=notepad@local",
            "commit", "--only", "-m", message, "--", str(relative_path)],
        cwd=repository,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        output = result.stdout + result.stderr

        if "nothing to commit" in output.lower():
            return False

        raise RuntimeError(
            output.strip() or "Git commit failed."
        )

    return True


def get_file_history(file_path, limit=20):
    """
    Retrieve the Git commit history of a specific file.
    """

    file_path = Path(file_path).resolve()

    if not file_path.exists() or not file_path.is_file():
        raise FileNotFoundError("File does not exist.")

    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=file_path.parent,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return []

    repository = Path(result.stdout.strip()).resolve()

    try:
        relative_path = file_path.relative_to(repository)
    except ValueError:
        return []

    result = subprocess.run(
        [
            "git",
            "log",
            f"-{limit}",
            "--follow",
            "--format=%H%x1f%h%x1f%an%x1f%aI%x1f%s",
            "--",
            str(relative_path)
        ],
        cwd=repository,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(
            result.stderr.strip() or "Could not retrieve file history."
        )

    history = []

    for line in result.stdout.splitlines():
        parts = line.split("\x1f", 4)

        if len(parts) != 5:
            continue

        history.append({
            "commit_hash": parts[0],
            "short_hash": parts[1],
            "author": parts[2],
            "date": parts[3],
            "message": parts[4]
        })

    return history


def get_file_version(file_path, commit_hash):
    """
    Retrieve the contents of a file from a particular Git commit.

    This does not modify the actual file on the computer.
    """

    file_path = Path(file_path).resolve()

    if not file_path.exists() or not file_path.is_file():
        raise FileNotFoundError("File does not exist.")

    # Find the existing Git repository.
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=file_path.parent,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError("Git repository not found.")

    repository = Path(result.stdout.strip()).resolve()

    try:
        relative_path = file_path.relative_to(repository)
    except ValueError:
        raise ValueError("File is outside the Git repository.")

    # Validate the requested commit.
    result = subprocess.run(
        [
            "git",
            "rev-parse",
            "--verify",
            f"{commit_hash}^{{commit}}"
        ],
        cwd=repository,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise ValueError("Invalid Git commit.")

    verified_commit = result.stdout.strip()

    # Retrieve the file contents from that commit.
    result = subprocess.run(
        [
            "git",
            "show",
            f"{verified_commit}:{relative_path.as_posix()}"
        ],
        cwd=repository,
        capture_output=True,
        text=True,
        encoding="utf-8"
    )

    if result.returncode != 0:
        raise RuntimeError(
            result.stderr.strip() or "Could not retrieve this file version."
        )

    return result.stdout


