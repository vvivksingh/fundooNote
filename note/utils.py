from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response

from user.utils import EncodeDecodeToken
import json
import logging
from .redis_server import RedisService


def verify_token(function):
    """
    this function is created for verifying user
    """

    def wrapper(self, request):
        if 'HTTP_AUTHORIZATION' not in request.META:
            msg = Response({'message': 'Token not provided in the header'})
            msg.status_code = 400
            return msg
        token = request.META['HTTP_AUTHORIZATION']
        user_id = EncodeDecodeToken.decode_token(token)
        request.data.update({'user_id': user_id.get("user_id")})
        request.data.update({'user_id': user_id.get("user_id")})
        return function(self, request)

    return wrapper


class RedisCache:
    def __init__(self):
        self.cache_memory = RedisService()

    def add_note(self, note):

        try:
            user_id = note.get("user_id")
            notes = self.get_note(user_id)
            note_id = note.get("id")
            notes.update({note_id: note})
            self.cache_memory.set(user_id, json.dumps(notes))

        except Exception as e:
            logging.error(e)

    def get_note(self, note_id):
        """
        getting notes from cache memory
        :param note:
        :return:
        """
        try:
            return json.loads(self.cache_memory.get(note_id))
        except Exception as e:
            logging.error(e)

    def update_note(self, user_id, updatednote):
        """
                for updating the note in cache
                :param user_id: id of note
                :param updatednote: note details
                """
        note_list = RedisService().get(user_id)
        if note_list is None:
            RedisService().redis_client.set(user_id, json.dumps([updatednote]))
            return
        for note in note_list:
            if updatednote.get(id) == note.get(id):
                note.update(updatednote)
        else:
            raise ObjectDoesNotExist

    def delete_note(self, user_id, note_id):
        """
        deleting the note from cache
        :param user_id: user id of Note user
        :param note_id: id of the note
        :return:
        """
        note_list = RedisService().redis_client.get(user_id)
        if note_list is None:
            raise ObjectDoesNotExist
        for note in note_list:
            if RedisService().redis_client.get(note_id) == note.get(id):
                del note
        else:
            raise ObjectDoesNotExist
