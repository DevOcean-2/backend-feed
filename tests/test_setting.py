from multiprocessing import Process
from time import sleep

import pytest
import uvicorn
from app.main import app
from app.utils.token import create_jwt_access_token


@pytest.fixture
def my_token(monkeypatch):
    monkeypatch.setenv("JWT_SECRET_KEY", "test_token")
    monkeypatch.setenv("JWT_EXPIRATION_DELTA", str(60))
    user_id = "test_user"

    token = create_jwt_access_token(user_id)
    return token


@pytest.fixture
def friend_token(monkeypatch):
    monkeypatch.setenv("JWT_SECRET_KEY", "test_token")
    monkeypatch.setenv("JWT_EXPIRATION_DELTA", str(60))
    user_id = "test_friend_user"

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