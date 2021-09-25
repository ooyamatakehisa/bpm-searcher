from injector import inject, singleton
from redis import Redis

from interface.repository.access_token_repository import AccessTokenRepository


@singleton
class AccessTokenRepositoryImpl(AccessTokenRepository):
    @inject
    def __init__(self, redis: Redis) -> None:
        self.redis = redis

    def create(self, access_token: str, ttl: float) -> None:
        self.redis.hset("access_token", "access_token", access_token)
        self.redis.hset("access_token", "ttl", ttl)

    def exist(self) -> bool:
        return self.redis.exists("access_token")

    def get(self) -> str:
        return self.redis.hget("access_token", "access_token")

    def get_ttl(self) -> float:
        return float(self.redis.hget("access_token", "ttl"))
