import json
import redis
from slugify import slugify


class RedisClient:
    def __init__(self, host='localhost', port=6379, db=0):
        self.r = redis.Redis(host=host, port=port, db=db)

    def set(self, key, value):
        self.r.set(key, json.dumps(value), 60)

    def get(self, key):
        try:
            value = self.r.get(key).decode('utf-8')
            return value
        except:
            return None
