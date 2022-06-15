from django.db import models
from user.models import NotesUser


class Note(models.Model):
    title = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=500, blank = True)
    user_id = models.ForeignKey(NotesUser, on_delete=models.CASCADE)
    color = models.CharField(default="red", max_length=20, blank=True)
    is_archived = models.BooleanField(default=False, blank= True)
