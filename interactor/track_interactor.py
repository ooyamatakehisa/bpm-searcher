from injector import inject, singleton
from logging import Logger
import requests

from envs import Envs
from interface.usecase.access_token_usecase import AccessTokenUsecase
from interface.usecase.track_usecase import TrackUsecase


@singleton
class TrackInteractor(TrackUsecase):
    @inject
    def __init__(
        self,
        envs: Envs,
        access_token_usecase: AccessTokenUsecase,
        logger: Logger,
    ) -> None:
        self.envs = envs
        self.access_token_usecase = access_token_usecase
        self.logger = logger

    def get_tracks(self, query: str) -> list:
        access_token = self.access_token_usecase.get_access_token()

        response = requests.get(
            "https://api.spotify.com/v1/search",
            headers={"Authorization": f"Bearer {access_token}"},
            params={
                "type": "track",
                "q": query,
            },
        )

        if response.status_code != requests.codes.ok:
            self.logger.error(
                f"cannot fetch search results correctly: {response.json()}"
            )

        items = response.json()["tracks"]["items"]
        if len(items) == 0:
            self.legger.info("no search result for the specified query.")
            return []

        response = requests.get(
            "https://api.spotify.com/v1/audio-features",
            headers={"Authorization": f"Bearer {access_token}"},
            params={
                "ids": ",".join(map(lambda item: item["id"], items)),
            },
        )

        if response.status_code != requests.codes.ok:
            self.logger.error(
                f"cannot fetch search result features correctly: {response.json()}"
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
