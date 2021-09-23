from injector import inject, singleton
from redis import Redis

from interface.repository.access_token_repository import AccessTokenRepository


@singleton
class AccessTokenRepositoryImpl(AccessTokenRepository):
    @inject
    def __init__(self, redis: Redis) -> None:
        self.redis = redis

    def create(self, access_token: str, ttl: float) -> None:
        value = {"access_token": access_token, "ttl": ttl}
        self.redis.hmset("access_token", value)

    def exist(self) -> bool:
        return self.redis.exists("access_token")

    def get(self) -> str:
        return self.redis.hget("access_token", "access_token")

    def get_ttl(self) -> float:
        return float(self.redis.hget("access_token", "ttl"))
