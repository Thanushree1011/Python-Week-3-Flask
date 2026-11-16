from app.file_manager import create_file, save_file
from app.git_manager import commit_file, get_file_history, get_file_version


def test_commit_history_and_version(tmp_path):
    f = tmp_path / "note.txt"
    create_file(str(f))
    save_file(str(f), "one")
    assert commit_file(str(f), "first") is True
    save_file(str(f), "two")
    assert commit_file(str(f), "second") is True

    history = get_file_history(str(f))
    assert [h["message"] for h in history] == ["second", "first"]
    assert get_file_version(str(f), history[1]["commit_hash"]) == "one"


def test_commit_without_changes_returns_false(tmp_path):
    f = tmp_path / "note.txt"
    create_file(str(f))
    save_file(str(f), "one")
    commit_file(str(f), "first")
    assert commit_file(str(f), "again") is False