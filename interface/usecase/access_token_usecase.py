from abc import ABCMeta, abstractmethod


class AccessTokenUsecase(metaclass=ABCMeta):
    @abstractmethod
    def get_access_token(self) -> str:
        pass
