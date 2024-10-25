from fastapi.testclient import TestClient
from app.main import app
from tests.test_setting import my_token, friend_token

client = TestClient(app)


def test_create_post(my_token):
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
        headers={"Authorization": f"Bearer {my_token}"}
    )
    assert response.status_code == 200
    print(response.json())
    test_delete_post(my_token, response.json()["post_id"])


def test_list_posts(friend_token):
    response = client.get(
        "http://127.0.0.1:8000/feed/posts?user_id=test_user",
        headers={"Authorization": f"Bearer {friend_token}"}
    )
    print(response.json())
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["post_id"] == 6


def test_update_post(my_token):
    content: str = "test #update content #lol"
    response = client.put(
        "http://127.0.0.1:8000/feed/posts/6",
        json={
            "content": content
        },
        headers={"Authorization": f"Bearer {my_token}"}
    )
    assert response.status_code == 200
    assert response.json()["content"] == content


def test_delete_post(my_token, post_id):
    response = client.delete(
        "http://127.0.0.1:8000/feed/posts/"+str(post_id),
        headers={"Authorization": f"Bearer {my_token}"}
    )

    assert response.status_code == 200


def test_like_post(friend_token):
    response = client.post(
        "http://127.0.0.1:8000/feed/posts/6/likes",
        json={
            "user_id": "test_friend_user",
            "nickname": "멍멍짱",
            "profile_image_url": "https://upload.wikimedia3.org"
        },
        headers={"Authorization": f"Bearer {friend_token}"}
    )
    assert response.status_code == 200
    assert response.json()['message'] == "Successfully liked a post"


def test_unlike_post(friend_token):
    response = client.delete(
        "http://127.0.0.1:8000/feed/posts/6/likes",
        headers={"Authorization": f"Bearer {friend_token}"}
    )
    assert response.status_code == 200
    assert response.json()['message'] == "Successfully unliked a post"
