from fastapi.testclient import TestClient
from app.main import app
from tests.test_setting import my_token, friend_token
from tests.test_posts import test_like_post, test_unlike_post

client = TestClient(app)


def test_get_notifications(my_token):
    response = client.get(
        "http://127.0.0.1:8000/feed/notifications",
        headers={"Authorization": f"Bearer {my_token}"}
    )
    assert response.status_code == 200

    return response


def test_mark_notification_as_read(my_token, friend_token):
    test_like_post(friend_token)

    notifications = test_get_notifications(my_token)
    assert len(notifications.json()[0]["likes"]) == 2
    assert notifications.json()[0]['is_read'] is False

    response = client.put(
        "http://127.0.0.1:8000/feed/notifications/6/read",
        headers={"Authorization": f"Bearer {my_token}"}
    )
    assert response.status_code == 200

    notifications = test_get_notifications(my_token)
    assert notifications.json()[0]['is_read'] is True

    test_unlike_post(friend_token)
    notifications = test_get_notifications(my_token)
    assert len(notifications.json()[0]["likes"]) == 1
    assert notifications.json()[0]['is_read'] is True
