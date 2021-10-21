from abc import ABCMeta, abstractmethod


class AuthUsecase(metaclass=ABCMeta):
    @abstractmethod
    def verify_user(self, id_token: str) -> dict:
        pass
