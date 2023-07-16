import os
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

from src.app import app
from src.database import Database


@pytest.fixture
def client(tmp_path: Path):
    db_path = tmp_path / "test.db"
    Database.initialize(str(db_path))

    yield TestClient(app)

    Database.terminate()
    os.remove(db_path)


class TestApp:
    def test_create_display_and_redirect(self, client: TestClient):
        link = "https://github.com/BURG3R5/url-shortener/"

        # Create
        create_response = client.post("/shorten", json={"original_url": link})
        assert create_response.status_code == 201
        back_half = create_response.json()["endpoint"]

        # Display
        display_response = client.get(f"/{back_half}/+")
        assert display_response.status_code == 200
        assert display_response.json() == {"original_url": link}

        # Redirect
        redirect_response = client.get(f"/{back_half}", follow_redirects=False)
        assert redirect_response.status_code == 307
        assert redirect_response.next_request.url == link  # type: ignore

    def test_display_fail(self, client: TestClient):
        response = client.get("/fake_back_half/+")

        assert response.status_code == 200
        with open("tests/golden_files/app_display_fail.txt", "rb") as golden_file:
            assert response.content == golden_file.read()

    def test_redirect_fail(self, client: TestClient):
        fake_back_half = "fake-back-half"

        response = client.get(f"/{fake_back_half}")

        assert response.status_code == 404
        assert response.json() == {"detail": "URL not found"}
