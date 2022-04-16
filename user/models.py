from django.db import models
from django.contrib.auth.models import User


class NotesUser(User):
    mobile = models.CharField(max_length=10)
    age = models.CharField(max_length=3)
