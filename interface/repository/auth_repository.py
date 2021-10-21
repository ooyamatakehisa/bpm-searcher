from abc import ABCMeta, abstractmethod


class AuthRepository(metaclass=ABCMeta):
    @abstractmethod
    def verify_user(self, id_token) -> dict:
        pass
