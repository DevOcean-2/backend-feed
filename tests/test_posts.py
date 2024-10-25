from multiprocessing import Process
from time import sleep

import pytest
import uvicorn
from fastapi.testclient import TestClient
from app.main import app
from app.utils.token import create_jwt_access_token

client = TestClient(app)


@pytest.fixture
def token(monkeypatch):
    monkeypatch.setenv("JWT_SECRET_KEY", "test_token")
    monkeypatch.setenv("JWT_EXPIRATION_DELTA", str(60))
    user_id = "test_user"

    token = create_jwt_access_token(user_id)
    return token


def run_server():
    uvicorn.run(app, host="127.0.0.1", port=8000)


@pytest.fixture(scope="module", autouse=True)
def start_server():
    server_process = Process(target=run_server)
    server_process.start()
    sleep(1)
    yield
    server_process.terminate()
    server_process.join()


def test_create_post(token):
    response = client.post(
        "http://127.0.0.1:8000/feed/posts",
        json={
            "image_urls": [
                "https://upload.wikimedia.org",
                "https://upload.wikimedia2.org",
                "https://upload.wikimedia3.org",
            ],
            "content": "test content #with #hashtag"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    print(response.json())
    test_delete_post(token, response.json()["post_id"])


def test_list_posts(token):
    response = client.get(
        "http://127.0.0.1:8000/feed/posts?user_id=test_user",
        headers={"Authorization": f"Bearer {token}"}
    )
    print(response.json())
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["post_id"] == 6


def test_update_post(token):
    content: str = "test #update content #lol"
    response = client.put(
        "http://127.0.0.1:8000/feed/posts/6",
        json={
            "content": content
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["content"] == content


def test_delete_post(token, post_id):
    response = client.delete(
        "http://127.0.0.1:8000/feed/posts/"+str(post_id),
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
