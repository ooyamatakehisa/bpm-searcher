import time

from injector import inject
import requests
from requests.auth import HTTPBasicAuth

from envs import Envs
from interface.usecase.ranking_usecase import RankingUsecase
from interface.repository.access_token_repository import AccessTokenRepository
from interface.repository.ranking_repository import RankingRepository


class RankingInteractor(RankingUsecase):
    @inject
    def __init__(
        self,
        env: Envs,
        access_token_repository: AccessTokenRepository,
        ranking_repository: RankingRepository
    ) -> None:
        self.env = env
        self.access_token_repository = access_token_repository
        self.ranking_repository = ranking_repository

    def get_ranking(self) -> list:
        if self.ranking_repository.exist():
            ranking_ttl = self.ranking_repository.get_ttl()

            # check if ranking should be updated
            if ranking_ttl > time.time():
                ranking = self.ranking_repository.get()
            else:
                ranking = self._create_ranking()

        else:
            ranking = self._create_ranking()

        return ranking

    def _create_ranking(self) -> list:
        if self.access_token_repository.exist():
            access_token_ttl = self.access_token_repository.get_ttl()

            # check if access token is expired
            if access_token_ttl > time.time():
                access_token = self.access_token_repository.get()
            else:
                access_token = self._create_spotify_access_token()

        else:
            access_token = self._create_spotify_access_token()

        global_charts_id = "37i9dQZEVXbMDoHDwVN2tF"
        response = requests.get(
            f"https://api.spotify.com/v1/playlists/{global_charts_id}",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        items = response.json()["tracks"]["items"]

        response = requests.get(
            "https://api.spotify.com/v1/audio-features",
            headers={"Authorization": f"Bearer {access_token}"},
            params={
                "ids": ",".join(map(lambda item: item["track"]["id"], items)),
            },
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

    def _create_spotify_access_token(self) -> str:
        response = requests.post(
            "https://accounts.spotify.com/api/token",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            auth=HTTPBasicAuth(self.env.CLIENT_ID, self.env.CLIENT_SECRET),
            data={"grant_type": "client_credentials"},
        )
        access_token = response.json()["access_token"]

        # spotify access token will expire after 1 hour and set ttl to 50 minutes
        ttl = time.time() + 60 * 50
        self.access_token_repository.create(access_token, ttl)
        return access_token
