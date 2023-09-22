import redis

from django.conf import settings


class RedisConnectionDB:
    def __init__(self, db=None):
        if not db or not isinstance(db, int):
            raise ValueError("Invalid db number")

        self.redis_conn = redis.Redis(host=settings.LOCAL_REDIS_HOST,
                                      port=settings.REDIS_PORT,
                                      db=db,
                                      password=settings.REDIS_PASSWORD)

    def setex_jti(self, jti, token_ttl, user_id):
        jti_claim = settings.SIMPLE_JWT['JTI_CLAIM']
        self.redis_conn.setex(f"{jti_claim}:{jti}", token_ttl, user_id)

    def get_jti(self, jti):
        jti_claim = settings.SIMPLE_JWT['JTI_CLAIM']
        jti_result = self.redis_conn.get(f"{jti_claim}:{jti}")
        if jti_result:
            return jti_result.decode("utf-8")

    def check_jti(self, jti):
        jti_claim = settings.SIMPLE_JWT['JTI_CLAIM']
        return self.redis_conn.exists(f"{jti_claim}:{jti}")
