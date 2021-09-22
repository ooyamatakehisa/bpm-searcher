from abc import ABCMeta, abstractmethod


class RankingRepository(metaclass=ABCMeta):
    @abstractmethod
    def create(self, ranking: list, ttl: float) -> None:
        pass

    @abstractmethod
    def exist(self) -> bool:
        pass

    @abstractmethod
    def get(self) -> dict:
        pass
