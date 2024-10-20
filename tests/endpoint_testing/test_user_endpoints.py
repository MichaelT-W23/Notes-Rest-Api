import json
import pytest

@pytest.mark.order(3)
def test_register_user(client):

    user_data = {
        "username": "testuser1",
        "email": "testuser1@example.com",
        "password": "testpassword1"
    }

    response = client.post('/users/register', data=json.dumps(user_data), content_type='application/json')

    print(f"Status Code: {response.status_code}")
    print(f"Response Data: {response.get_data(as_text=True)}")

    assert response.status_code == 201
    assert response.json["username"] == "testuser1"
    assert "user_id" in response.json


@pytest.mark.order(4)
def test_register_user_existing_username(client):

    user_data = {
        "username": "testuser2",
        "email": "testuser2@example.com",
        "password": "testpassword2"
    }

    client.post('/users/register', data=json.dumps(user_data), content_type='application/json')

    response = client.post('/users/register', data=json.dumps(user_data), content_type='application/json')

    assert response.status_code == 400
    assert response.json["error"] == "Username already exists"
