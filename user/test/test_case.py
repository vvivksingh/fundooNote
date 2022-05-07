import pytest
from rest_framework.reverse import reverse
from ..models import NotesUser


@pytest.mark.django_db
class TestUser:

    def test_userRegistration(self, client):
        # test case create their own database to test the views
        url = reverse("registration")
        user = {
            "username": "vivek",
            "password": "vivek123",
            "age": 27,
            "email": "vvivksingh@gmail.com",
            "first_name": "Vivek",
            "last_name": "Singh",
            "mobile": "9039165805"
        }
        response = client.post(url, user)
        assert response.status_code == 201

    def test_login(self, client):
        # test the login
        user = NotesUser.objects.create_user(username="vivek",
                                             password="vivek123",
                                             age=27,
                                             email="vvivksingh@gmail.com",
                                             first_name="Vivek",
                                             last_name="Singh",
                                             mobile="9039165805")
        login_data = {
            "username": "vivek",
            "password": "vivek123",
        }
        url = reverse("login")
        response = client.post(url, login_data)
        assert response.status_code == 200