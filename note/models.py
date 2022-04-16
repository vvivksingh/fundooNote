from django.db import models
from user.models import NotesUser


class Note(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    user_id = models.ForeignKey(NotesUser, on_delete=models.CASCADE)
