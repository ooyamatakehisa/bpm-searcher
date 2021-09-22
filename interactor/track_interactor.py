import time

from injector import inject
import requests
from requests.auth import HTTPBasicAuth

from envs import Envs
from interface.usecase.track_usecase import TrackUsecase
from interface.repository.access_token_repository import AccessTokenRepository


class TrackInteractor(TrackUsecase):
    @inject
    def __init__(
        self,
        envs: Envs,
        access_token_repository: AccessTokenRepository
    ) -> None:
        self.envs = envs
        self.access_token_repository = access_token_repository

    def get_tracks(self, query: str) -> list:
        if self.access_token_repository.exist():
            access_token_ttl = self.access_token_repository.get_ttl()

            # check if access token is expired
            if access_token_ttl > time.time():
                access_token = self._create_spotify_access_token()
            else:
                access_token = self.access_token_repository.get()

        else:
            access_token = self._create_spotify_access_token()

        response = requests.get(
            "https://api.spotify.com/v1/search",
            headers={"Authorization": f"Bearer {access_token}"},
            params={
                "type": "track",
                "q": query,
            },
        )
        items = response.json()["tracks"]["items"]
        if len(items) == 0:
            return []

        response = requests.get(
            "https://api.spotify.com/v1/audio-features",
            headers={"Authorization": f"Bearer {access_token}"},
            params={
                "ids": ",".join(map(lambda item: item["id"], items)),
            },
        )

        features = response.json()["audio_features"]

        tracks = []
        for idx, item in enumerate(items):
            spotify_id = item["id"]
            song_name = item["name"]
            artist = item["artists"][0]["name"]
            image_url = item["album"]["images"][0]["url"]
            album_name = item["album"]["name"]
            preview_url = item["preview_url"]

            tracks.append({
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

        return tracks

    def _create_spotify_access_token(self) -> str:
        response = requests.post(
            "https://accounts.spotify.com/api/token",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            auth=HTTPBasicAuth(self.envs.CLIENT_ID, self.envs.CLIENT_SECRET),
            data={"grant_type": "client_credentials"},
        )
        access_token = response.json()["access_token"]

        # spotify access token will expire after 1 hour and set ttl to 50 minutes
        ttl = time.time() + 60 * 50
        self.access_token_repository.create(access_token, ttl)
        return access_token
