from logging import Logger
import time

from injector import inject, singleton
from redis import Redis
import requests
from requests.auth import HTTPBasicAuth

from envs import Envs
from interface.repository.access_token_repository import AccessTokenRepository


@singleton
class AccessTokenRepositoryImpl(AccessTokenRepository):
    @inject
    def __init__(self, envs: Envs, logger: Logger, redis: Redis) -> None:
        self.envs = envs
        self.logger = logger
        self.redis = redis

    def get_access_token(self) -> str:
        if self._valid_cache():
            access_token = self._get_access_token_from_cache()

        else:
            self.logger.info("access_token cache is not valid and create new one.")
            access_token = self._get_access_token_from_spotify()
            self._save_cache(access_token)

        return access_token

    def _get_access_token_from_cache(self) -> str:
        return self.redis.hget("access_token", "access_token")

    def _get_access_token_from_spotify(self) -> str:
        response = requests.post(
            "https://accounts.spotify.com/api/token",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            auth=HTTPBasicAuth(self.envs.CLIENT_ID, self.envs.CLIENT_SECRET),
            data={"grant_type": "client_credentials"},
        )

        if response.status_code != requests.codes.ok:
            self.logger.error(f"cannot fetch access_token correctly: {response.json()}")

        access_token = response.json()["access_token"]
        return access_token

    def _save_cache(self, access_token: str) -> None:
        # spotify access token will expire after 1 hour and set ttl to 50 min
        ttl = time.time() + 60 * 50

        self.redis.hset("access_token", "access_token", access_token)
        self.redis.hset("access_token", "ttl", ttl)

    def _valid_cache(self) -> bool:
        """Check if cache exists and is not expired

        Returns:
            bool: True if chache exists and is not expired
        """
        if not self.redis.exists("access_token"):
            return False

        ttl = float(self.redis.hget("access_token", "ttl"))
        return ttl > time.time()
