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

    def get_features_by_ids(self, ids: list, access_token: str = None):
        if access_token is None:
            access_token = self.access_token_usecase.get_access_token()

        response = requests.get(
            "https://api.spotify.com/v1/audio-features",
            headers={"Authorization": f"Bearer {access_token}"},
            params={
                "ids": ",".join(ids),
            },
        )

        if response.status_code != requests.codes.ok:
            self.logger.error(
                f"cannot fetch search result features correctly: {response.json()}"
            )

        features = response.json()["audio_features"]
        return features

    def get_tracks_by_ids(self, ids: list) -> list:
        self.logger.error(ids)
        access_token = self.access_token_usecase.get_access_token()

        response = requests.get(
            "https://api.spotify.com/v1/tracks",
            headers={"Authorization": f"Bearer {access_token}"},
            params={
                "ids": ",".join(ids),
            },
        )

        if response.status_code != requests.codes.ok:
            self.logger.error(
                f"cannot fetch tracks by ids correctly: {response.json()}"
            )

        items = response.json()["tracks"]
        features = self.get_features_by_ids(ids)

        tracks = [
            {
                "spotify_id": item["id"],
                "song_name": item["name"],
                "album_name": item["album"]["name"],
                "artist": item["artists"][0]["name"],
                "bpm": features[idx]["tempo"],
                "key": features[idx]["key"],
                "mode": features[idx]["mode"],
                "image_url": item["album"]["images"][0]["url"],
                "preview_url": item["preview_url"],
                "danceability": features[idx]["danceability"],
                "energy": features[idx]["energy"],
            }
            for idx, item in enumerate(items)
        ]

        return tracks

    def get_tracks_by_query(self, query: str) -> list:
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
            self.logger.info("no search result for the specified query.")
            return []

        ids = map(lambda item: item["id"], items)
        features = self.get_features_by_ids(ids)

        tracks = [
            {
                "spotify_id": item["id"],
                "song_name": item["name"],
                "album_name": item["album"]["name"],
                "artist": item["artists"][0]["name"],
                "bpm": features[idx]["tempo"],
                "key": features[idx]["key"],
                "mode": features[idx]["mode"],
                "image_url": item["album"]["images"][0]["url"],
                "preview_url": item["preview_url"],
                "danceability": features[idx]["danceability"],
                "energy": features[idx]["energy"],
            }
            for idx, item in enumerate(items)
        ]

        return tracks
