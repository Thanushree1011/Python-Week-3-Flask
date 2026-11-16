import pytest

from app import create_app


@pytest.fixture
def client():
    return create_app().test_client()


def test_save_creates_commit(client, tmp_path):
    f = str(tmp_path / "a.txt")
    assert client.post("/api/files/create", json={"path": f}).status_code == 201
    r = client.post("/api/files/save", json={"path": f, "content": "hi"}).get_json()
    assert r["changed"] and r["git_committed"] and r["git_error"] is None
    h = client.post("/api/files/history", json={"path": f}).get_json()
    assert h["count"] == 2


def test_directory_list_returns_path(client, tmp_path):
    r = client.post("/api/directory/list", json={"path": str(tmp_path)}).get_json()
    assert r["path"] == str(tmp_path.resolve())