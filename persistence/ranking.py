from injector import inject
import json
from redis import Redis

from interface.repository.ranking_repository import RankingRepository


class RankingRepositoryImpl(RankingRepository):
    @inject
    def __init__(self, redis: Redis) -> None:
        self.redis = redis

    def create(self, ranking: list, ttl: float) -> None:
        ranking_str = json.dumps(ranking)
        value = {"ranking": ranking_str, "ttl": ttl}
        self.redis.hmset("ranking", value)

    def exist(self) -> bool:
        return self.redis.exists("ranking")

    def get(self) -> dict:
        ranking_str = self.redis.hget("ranking", "ranking")
        return json.loads(ranking_str)

    def get_ttl(self) -> float:
        return float(self.redis.hget("ranking", "ttl"))
