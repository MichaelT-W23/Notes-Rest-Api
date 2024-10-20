import json
import pytest

@pytest.mark.order(1)
def test_get_notes_by_user(client):

    user_data = {
        "username": "testuser3",
        "email": "testuser3@example.com",
        "password": "testpassword3"
    }

    response = client.post('/users/register', data=json.dumps(user_data), content_type='application/json')
    user_id = response.json["user_id"]

    response = client.get(f'/users/{user_id}/notes')

    assert response.status_code == 200
    assert isinstance(response.json, list)


@pytest.mark.order(2)
def test_get_notes_by_user_no_notes(client):

    user_data = {
        "username": "testuser4",
        "email": "testuser4@example.com",
        "password": "testpassword4"
    }

    response = client.post('/users/register', data=json.dumps(user_data), content_type='application/json')
    user_id = response.json["user_id"]


    response = client.get(f'/users/{user_id}/notes')

    assert response.status_code == 200
    assert response.json == []
