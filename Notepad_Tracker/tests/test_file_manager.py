import pytest

from app.file_manager import create_file, read_file, save_file, create_folder, list_directory


def test_create_and_read(tmp_path):
    f = tmp_path / "a.txt"
    create_file(str(f))
    assert read_file(str(f)) == ""


def test_create_existing_file_fails(tmp_path):
    f = tmp_path / "a.txt"
    create_file(str(f))
    with pytest.raises(FileExistsError):
        create_file(str(f))


def test_save_reports_change(tmp_path):
    f = tmp_path / "a.txt"
    create_file(str(f))
    assert save_file(str(f), "hello") is True
    assert save_file(str(f), "hello") is False
    assert read_file(str(f)) == "hello"


def test_relative_path_rejected():
    with pytest.raises(ValueError):
        create_file("relative.txt")


def test_non_utf8_file(tmp_path):
    f = tmp_path / "bin.txt"
    f.write_bytes(b"\xff\xfe\x00\x80")
    with pytest.raises(ValueError):
        read_file(str(f))


def test_folder_and_listing(tmp_path):
    create_folder(str(tmp_path / "sub"))
    create_file(str(tmp_path / "b.txt"))
    items = list_directory(str(tmp_path))
    assert [i["type"] for i in items] == ["folder", "file"]