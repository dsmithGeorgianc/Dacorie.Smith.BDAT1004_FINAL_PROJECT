import redis
import json

import logging

logger = logging.getLogger(__name__)


class RedisHelper:
    def __init__(self, host='redis', port=6379, db=0, password=None):
        self.r = redis.StrictRedis(host=host, port=port, db=db, password=password, decode_responses=True)

    def set_to_cache(self, key, value, expiry_seconds=None):
        value_str = json.dumps(value)
        if expiry_seconds:
            self.r.setex(key, expiry_seconds, value_str)
        else:
            self.r.set(key, value_str)

    def get_from_cache(self, key):
        result = self.r.get(key)
        return json.loads(result) if result else None

    def delete_from_cache(self, key):
        self.r.delete(key)

    def exists_in_cache(self, key):
        return self.r.exists(key)
