import redis
from redis.exceptions import ConnectionError

from django.conf import settings


class RedisConnectionDB:
    def __init__(self):
        #TODO: add host
        self.client = redis.Redis(host='redis-taskflow',
                                  port=settings.REDIS_PORT,
                                  password=settings.REDIS_PASSWORD)

    def setex_jti(self, jti, token_ttl, user_id):
        jti_claim = settings.SIMPLE_JWT['JTI_CLAIM']
        self.client.setex(f"{jti_claim}:{jti}", token_ttl, user_id)

    def get_jti(self, jti):
        jti_claim = settings.SIMPLE_JWT['JTI_CLAIM']
        jti_result = self.client.get(f"{jti_claim}:{jti}")
        if jti_result:
            return jti_result.decode("utf-8")

    def check_jti(self, jti):
        jti_claim = settings.SIMPLE_JWT['JTI_CLAIM']
        return self.client.exists(f"{jti_claim}:{jti}")
