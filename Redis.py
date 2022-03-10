import json
import redis


class RedisClient:
    def __init__(self, host='localhost', port=6379, db=0):
        self.r = redis.Redis(host=host, port=port, db=db)

    def set(self, key, value):
        self.r.set(key, json.dumps(value), 60)

    def get(self, key):
        try:
            return self.r.get(key).decode('utf-8')
        except:
            return None
