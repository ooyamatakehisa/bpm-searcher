from injector import inject, singleton
import json
from redis import Redis

from interface.repository.ranking_repository import RankingRepository


@singleton
class RankingRepositoryImpl(RankingRepository):
    @inject
    def __init__(self, redis: Redis) -> None:
        self.redis = redis

    def create(self, ranking: list, ttl: float) -> None:
        ranking_str = json.dumps(ranking)
        self.redis.hset("ranking", "ranking", ranking_str)
        self.redis.hset("ranking", "ttl", ttl)

    def exist(self) -> bool:
        return self.redis.exists("ranking")

    def get(self) -> dict:
        ranking_str = self.redis.hget("ranking", "ranking")
        return json.loads(ranking_str)

    def get_ttl(self) -> float:
        return float(self.redis.hget("ranking", "ttl"))
