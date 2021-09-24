import time

from injector import inject, singleton
from logging import Logger
import requests
from requests.auth import HTTPBasicAuth

from envs import Envs
from interface.usecase.access_token_usecase import AccessTokenUsecase
from interface.repository.access_token_repository import AccessTokenRepository


@singleton
class AccessTokenInteractor(AccessTokenUsecase):
    @inject
    def __init__(
        self,
        envs: Envs,
        access_token_repository: AccessTokenRepository,
        logger: Logger,
    ) -> None:
        self.envs = envs
        self.access_token_repository = access_token_repository
        self.logger = logger

    def get_access_token(self) -> str:
        if self.access_token_repository.exist():
            access_token_ttl = self.access_token_repository.get_ttl()

            # check if access token is expired
            if access_token_ttl > time.time():
                access_token = self.access_token_repository.get()
            else:
                self.logger.info("access_token is expired and create new one.")
                access_token = self._create_spotify_access_token()

        else:
            self.logger.info("access_token doesn't exist and create new one.")
            access_token = self._create_spotify_access_token()

        return access_token

    def _create_spotify_access_token(self) -> str:
        response = requests.post(
            "https://accounts.spotify.com/api/token",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            auth=HTTPBasicAuth(self.envs.CLIENT_ID, self.envs.CLIENT_SECRET),
            data={"grant_type": "client_credentials"},
        )

        if response.status_code != requests.codes.ok:
            self.logger.error(f"cannot fetch access_token correctly: {response.json()}")

        access_token = response.json()["access_token"]

        # spotify access token will expire after 1 hour and set ttl to 50 minutes
        ttl = time.time() + 60 * 50
        self.access_token_repository.create(access_token, ttl)
        return access_token
