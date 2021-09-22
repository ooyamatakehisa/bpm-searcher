from abc import ABCMeta, abstractmethod


class AccessTokenRepository(metaclass=ABCMeta):
    @abstractmethod
    def create(self, access_token: str, ttl: float) -> None:
        pass

    @abstractmethod
    def exist(self) -> bool:
        pass

    @abstractmethod
    def get(self) -> str:
        pass

    @abstractmethod
    def get_ttl(self) -> float:
        pass
