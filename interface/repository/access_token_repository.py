from abc import ABCMeta, abstractmethod


class AccessTokenRepository(metaclass=ABCMeta):
    @abstractmethod
    def get_access_token(self) -> str:
        """Get access token of Spotify

        Returns:
            str: spotify access token
        """
        pass
