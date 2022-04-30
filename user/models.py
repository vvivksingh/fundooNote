from datetime import datetime

from django.db import models
from django.contrib.auth.models import User


class NotesUser(User):
    mobile = models.CharField(max_length=10)
    age = models.CharField(max_length=3)


class LogTable(models.Model):
    hit_time = models.DateTimeField(default=datetime.now, blank=True)
    type_of_request = models.CharField(max_length=250)
    response = models.CharField(max_length=200)
