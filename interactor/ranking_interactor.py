import time

from injector import inject, singleton
from logging import Logger
import requests

from envs import Envs
from interface.repository.access_token_repository import AccessTokenRepository
from interface.usecase.ranking_usecase import RankingUsecase
from interface.repository.ranking_repository import RankingRepository


@singleton
class RankingInteractor(RankingUsecase):
    @inject
    def __init__(
        self,
        env: Envs,
        access_token_repository: AccessTokenRepository,
        ranking_repository: RankingRepository,
        logger: Logger,
    ) -> None:
        self.env = env
        self.access_token_repository = access_token_repository
        self.ranking_repository = ranking_repository
        self.logger = logger

    def get_ranking(self) -> list:
        if self.ranking_repository.exist():
            ranking_ttl = self.ranking_repository.get_ttl()

            # check if ranking should be updated
            if ranking_ttl > time.time():
                ranking = self.ranking_repository.get()
            else:
                self.logger.info("ranking is expired and create new one.")
                ranking = self._create_ranking()

        else:
            self.logger.info("ranking doesn't exist and create new one.")
            ranking = self._create_ranking()

        return ranking

    def _create_ranking(self) -> list:
        access_token = self.access_token_repository.get_access_token()

        global_charts_id = "37i9dQZEVXbMDoHDwVN2tF"
        response = requests.get(
            f"https://api.spotify.com/v1/playlists/{global_charts_id}",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        if response.status_code != requests.codes.ok:
            self.logger.error(f"cannot fetch ranking correctly: {response.json()}")

        items = response.json()["tracks"]["items"]

        response = requests.get(
            "https://api.spotify.com/v1/audio-features",
            headers={"Authorization": f"Bearer {access_token}"},
            params={
                "ids": ",".join(map(lambda item: item["track"]["id"], items)),
            },
        )

        if response.status_code != requests.codes.ok:
            self.logger.error(
                f"cannot fetch ranking features correctly: {response.json()}"
            )

        features = response.json()["audio_features"]

        ranking = []
        for idx, item in enumerate(items):
            spotify_id = item["track"]["id"]
            song_name = item["track"]["name"]
            artist = item["track"]["artists"][0]["name"]
            image_url = item["track"]["album"]["images"][0]["url"]
            album_name = item["track"]["album"]["name"]
            preview_url = item["track"]["preview_url"]

            ranking.append({
                "spotify_id": spotify_id,
                "song_name": song_name,
                "album_name": album_name,
                "artist": artist,
                "bpm": features[idx]["tempo"],
                "key": features[idx]["key"],
                "mode": features[idx]["mode"],
                "image_url": image_url,
                "preview_url": preview_url,
                "danceability": features[idx]["danceability"],
                "energy": features[idx]["energy"],
            })

        # expire cache after 6 hours
        ttl = time.time() + 60 * 60 * 6
        self.ranking_repository.create(ranking, ttl)
        return ranking
