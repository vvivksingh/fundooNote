import json

import redis


class RedisService:
    def __init__(self):
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)

    def set(self, key, value):
        return self.redis_client.set(key, value)

    def get(self, user_id):
        return self.redis_client.get(user_id)

    def delete(self, user_id, note_id):
        notes = dict(self.get(user_id))
        del notes[str(note_id)]
        return self.set(user_id, json.dumps(notes))
