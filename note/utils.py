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

    def wrapper(self, request, *args, **kwargs):

        if 'HTTP_AUTHORIZATION' not in request.META:
            msg = Response({'message': 'Token not provided in the header'})
            msg.status_code = 400
            return msg
        token = request.META['HTTP_AUTHORIZATION']
        user_id = EncodeDecodeToken.decode_token(token)
        request.data.update({'user_id': user_id.get("user_id")})
        request.data.update({'user_id': user_id.get("user_id")})
        return function(self, request, *args, **kwargs)

    return wrapper


class RedisCache:
    # def __init__(self):
    #     self.cache_memory = RedisService()

    cache_mem = RedisService()

    @classmethod
    def add_note(cls, note):

        try:
            print(note)
            user_id = int(note.get("user_id"))
            notes = {} if cls.get_note(user_id) is None else cls.get_note(user_id)
            # if cls.get_note(user_id) is None:
            #     notes = {}
            # else:
            #     notes = cls.get_note(user_id)

            note_id = note.get("id")

            notes.update({note_id: note})
            cls.cache_mem.set(user_id, json.dumps(notes))

        except Exception as e:
            logging.error(e)

    @classmethod
    def get_note(cls, user_id):
        """
        getting notes from cache memory
        :param note:
        :return:
        """
        try:
            return json.loads(cls.cache_mem.get(user_id))
        except Exception as e:
            logging.error(e)




    @classmethod
    def update_note(cls, updated_note):

        try:
            print(updated_note)
            user_id = updated_note.get('user_id')
            id = str(updated_note.get("id"))
            note_dict = json.loads(RedisService().get(user_id))
            print(note_dict)
            if note_dict.get(id):
                note_dict.update({id: updated_note})
                cls.cache_mem.set(user_id, json.dumps(note_dict))
        except Exception as e:
            logging.error(e)

    @classmethod
    def delete_note(cls, user_id, note_id):
        """
        deleting the note from cache
        :param user_id: user id of Note user
        :param note_id: id of the note
        :return:
        """
        note_dict = cls.cache_mem.get(user_id)
        note_dict = json.loads(note_dict)
        print(note_dict)
        if note_dict is not None:
            del note_dict[note_id]
            cls.cache_mem.set(user_id, json.dumps(note_dict))
        else:
            raise ObjectDoesNotExist
