from rest_framework import serializers
from . models import Note


class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['title', 'description', 'user_id', "id", 'color', 'is_archived']
        read_only_fields = ["id"]