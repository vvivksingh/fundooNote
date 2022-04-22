import redis


class RedisService:
    def __init__(self):
        self.redis_client = redis.Redis(host='localhost', port=6379)

    def set(self, key, value):
        return self.redis_client.set(key, value)

    def get(self, key):
        return self.redis_client.get(key)

    def put(self, key, value):
        return self.redis_client.set(key, value)

    def delete(self, key):
        return self.redis_client.delete(key)
