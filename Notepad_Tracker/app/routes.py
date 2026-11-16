
from pathlib import Path

from flask import Blueprint, jsonify, render_template, request

from app.file_manager import (
    create_file,
    read_file,
    save_file,
    create_folder,
    list_directory
)

from app.git_manager import commit_file, get_file_history


main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html")


# Create a new file
@main.route("/api/files/create", methods=["POST"])
def create_new_file():

    data = request.get_json(silent=True) or {}
    file_path = data.get("path")

    try:
        path = create_file(file_path)

        git_committed = False
        git_error = None

        try:
            git_committed = commit_file(
                path,
                "Created " + path.name
            )
        except (RuntimeError, FileNotFoundError, ValueError) as error:
            git_error = str(error)

        return jsonify({
            "success": True,
            "message": "File created successfully.",
            "path": str(path),
            "git_committed": git_committed,
            "git_error": git_error
        }), 201

    except (ValueError, FileExistsError, FileNotFoundError, OSError) as error:
        return jsonify({
            "success": False,
            "error": str(error)
        }), 400


# Open an existing file
@main.route("/api/files/open", methods=["POST"])
def open_existing_file():

    data = request.get_json(silent=True) or {}
    file_path = data.get("path")

    try:
        content = read_file(file_path)

        return jsonify({
            "success": True,
            "path": str(Path(file_path).expanduser().resolve()),
            "content": content
        }), 200

    except FileNotFoundError as error:
        return jsonify({
            "success": False,
            "error": str(error)
        }), 404

    except (ValueError, OSError) as error:
        return jsonify({
            "success": False,
            "error": str(error)
        }), 400


# Save file contents
@main.route("/api/files/save", methods=["POST"])
def save_existing_file():

    data = request.get_json(silent=True) or {}

    file_path = data.get("path")
    content = data.get("content")

    if not isinstance(content, str):
        return jsonify({
            "success": False,
            "error": "File content must be a string."
        }), 400

    try:
        changed = save_file(file_path, content)

        git_committed = False
        git_error = None

        if changed:
            try:
                git_committed = commit_file(
                    file_path,
                    "Updated " + Path(file_path).name
                )
            except (RuntimeError, FileNotFoundError, ValueError) as error:
                git_error = str(error)

        return jsonify({
            "success": True,
            "message": "File saved successfully.",
            "changed": changed,
            "git_committed": git_committed,
            "git_error": git_error
        }), 200

    except FileNotFoundError as error:
        return jsonify({
            "success": False,
            "error": str(error)
        }), 404

    except (ValueError, OSError) as error:
        return jsonify({
            "success": False,
            "error": str(error)
        }), 400


# Get Git history for a file
@main.route("/api/files/history", methods=["POST"])
def get_file_history_api():

    data = request.get_json(silent=True) or {}

    file_path = data.get("path")
    limit = data.get("limit", 20)

    if not isinstance(file_path, str) or not file_path.strip():
        return jsonify({
            "success": False,
            "error": "A valid file path is required."
        }), 400

    try:
        limit = int(limit)

        if limit < 1 or limit > 100:
            return jsonify({
                "success": False,
                "error": "History limit must be between 1 and 100."
            }), 400

        history = get_file_history(file_path, limit)

        return jsonify({
            "success": True,
            "path": str(Path(file_path).expanduser().resolve()),
            "count": len(history),
            "history": history
        }), 200

    except FileNotFoundError as error:
        return jsonify({
            "success": False,
            "error": str(error)
        }), 404

    except (ValueError, OSError) as error:
        return jsonify({
            "success": False,
            "error": str(error)
        }), 400

    except RuntimeError as error:
        return jsonify({
            "success": False,
            "error": str(error)
        }), 500


# Create a new folder
@main.route("/api/folders/create", methods=["POST"])
def create_new_folder():

    data = request.get_json(silent=True) or {}
    folder_path = data.get("path")

    try:
        folder = create_folder(folder_path)

        return jsonify({
            "success": True,
            "message": "Folder created successfully.",
            "path": str(folder)
        }), 201

    except FileExistsError as error:
        return jsonify({
            "success": False,
            "error": str(error)
        }), 409

    except (ValueError, FileNotFoundError, OSError) as error:
        return jsonify({
            "success": False,
            "error": str(error)
        }), 400


# List files and folders in a directory
@main.route("/api/directory/list", methods=["POST"])
def get_directory_contents():

    data = request.get_json(silent=True) or {}
    directory_path = data.get("path")

    try:
        items = list_directory(directory_path)

        return jsonify({"success": True,
                "path": str(Path(directory_path).expanduser().resolve()),
                "items": items}), 200

    except FileNotFoundError as error:
        return jsonify({
            "success": False,
            "error": str(error)
        }), 404

    except (ValueError, OSError) as error:
        return jsonify({
            "success": False,
            "error": str(error)
        }), 400
