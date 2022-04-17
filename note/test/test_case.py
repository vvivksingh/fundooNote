import json

import pytest

from rest_framework.reverse import reverse
from user.models import NotesUser
from ..models import Note


class TestNotes:

    @pytest.mark.django_db
    def test_create_user_and_notes(self, client):
        user = NotesUser.objects.create_user(username="vivek",
                                             password="vivek123",
                                             age=27,
                                             email="vvivksingh@gmail.com",
                                             first_name="Vivek",
                                             last_name="Singh",
                                             mobile="9039165805")
        user.is_verified = True
        user.save()
        note = {"title": "my notes", "description": "test notes", "user_id": user.id}
        url = reverse("notes")
        response = client.post(url, note)
        assert response.status_code == 201

    @pytest.mark.django_db
    def test_get_notes(self, client):
        url = reverse("notes")
        user = NotesUser.objects.create_user(username="vivek",
                                             password="vivek123",
                                             age=27,
                                             email="vvivksingh@gmail.com",
                                             first_name="Vivek",
                                             last_name="Singh",
                                             mobile="9039165805")
        user.save()
        note = Note.objects.create(
            title="my notes", description="test notes", user_id=user
        )
        note.save()
        get_note = {"user_id": user.id}
        response = client.get(url, get_note)
        print(response.content)
        assert response.status_code == 201

    @pytest.mark.django_db
    def test_to_delete_an_existing_note(self, client):
        # creating user
        user = NotesUser.objects.create_user(username="vivek",
                                             password="vivek123",
                                             age=27,
                                             email="vvivksingh@gmail.com",
                                             first_name="Vivek",
                                             last_name="Singh",
                                             mobile="9039165805")
        user.is_verified = True
        user.save()

        # adding notes
        note = Note.objects.create(
            title="my notes", description="test notes", user_id=user
        )
        note.save()
        url = reverse("notes")
        # deleting existing note
        delete_note_data = {
            "id": note.id
        }
        data = json.dumps(delete_note_data)
        response = client.delete(url, data, content_type="application/json")
        assert response.status_code == 204
