import json

import pytest

from rest_framework.reverse import reverse
from user.models import NotesUser


def gen_header(client):
    NotesUser.objects.create_user(username="vivek",
                                  password="vivek123",
                                  age=27,
                                  email="vvivksingh@gmail.com",
                                  first_name="Vivek",
                                  last_name="Singh",
                                  mobile="9039165805")
    auth_response = client.post(reverse("login"), {
        "username": "vivek",
        "password": "vivek123",
    })
    msg = auth_response.data.get("message")
    token = auth_response.data.get("token")
    header = {'HTTP_AUTHORIZATION': token, 'content_type': 'application/json'}

    return header


class TestNotes:

    @pytest.mark.django_db
    def test_create_notes(self, client):
        note_payload = {"title": "my notes", "description": "test notes"}
        url = reverse("notes")
        header = gen_header(client)
        response = client.post(url, note_payload, **header)
        assert response.data["data"]["title"] == note_payload["title"]
        assert response.status_code == 201


    @pytest.mark.django_db
    def test_get_notes(self, client):
        url = reverse("notes")

        note_payload = {"title": "my notes", "description": "test notes"}
        header = gen_header(client)
        client.post(url, note_payload, **header)
        client.post(url, note_payload, **header)
        client.post(url, note_payload, **header)
        client.post(url, note_payload, **header)
        client.post(url, note_payload, **header)
        response = client.get(url, **header)
        assert len(response.data["data"]) == 5
        assert response.status_code == 200


    @pytest.mark.django_db
    def test_to_delete_an_existing_note(self, client):
        url = reverse("notes")
        note_payload = {"title": "my notes", "description": "test notes"}
        header = gen_header(client)
        response = client.post(url, note_payload, **header)

        response = client.delete(url, data=json.dumps({"id": response.data["data"].get("id")}), **header)
        assert response.status_code == 204

    @pytest.mark.django_db
    def test_to_update_note(self, client):
        url = reverse("notes")
        note_payload = {"title": "my notes", "description": "test notes"}
        header = gen_header(client)
        response = client.post(url, note_payload, **header)
        json_data = json.loads(response.content)
        id = json_data.get('data').get("id")
        updated_data = {
            "title": "my notes",
            "description": "updated test note",
            "id": int(id)
        }
        response = client.put(url, updated_data, **header)
        assert response.status_code == 201
