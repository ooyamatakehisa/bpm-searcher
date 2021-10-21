from logging import Logger
from typing import List

from injector import inject, singleton
import requests

from domain.model.track import Track
from interface.repository.access_token_repository import AccessTokenRepository


@singleton
class TrackRepositoryImpl:
    @inject
    def __init__(self, logger: Logger, access_token_repository: AccessTokenRepository):
        self.logger = logger
        self.access_token_repository = access_token_repository

    def _get_feature_by_id(self, spotify_id: str, access_token: str = None) -> dict:
        if access_token is None:
            access_token = self.access_token_repository.get_access_token()

        response = requests.get(
            f"https://api.spotify.com/v1/audio-features/{spotify_id}",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        if response.status_code != requests.codes.ok:
            self.logger.error(
                f"cannot fetch search a result feature correctly: {response.json()}"
            )

        feature = response.json()
        return feature

    def _get_features_by_ids(
        self,
        ids: List[str],
        access_token: str = None,
    ) -> List[dict]:
        if access_token is None:
            access_token = self.access_token_repository.get_access_token()

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

    def get_track_by_id(self, track_id: str) -> Track:
        spotify_id = track_id
        access_token = self.access_token_repository.get_access_token()

        response = requests.get(
            f"https://api.spotify.com/v1/tracks/{spotify_id}",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        if response.status_code != requests.codes.ok:
            self.logger.error(
                f"cannot fetch tracks by ids correctly: {response.json()}"
            )
        track_data = response.json()

        feature = self._get_feature_by_id(spotify_id)

        return Track(
            spotify_id=track_data["id"],
            song_name=track_data["name"],
            album_name=track_data["album"]["name"],
            artist=track_data["artists"][0]["name"],
            bpm=feature["tempo"],
            key=feature["key"],
            mode=feature["mode"],
            image_url=track_data["album"]["images"][0]["url"],
            preview_url=track_data["preview_url"],
            danceability=feature["danceability"],
            energy=feature["energy"],
        )

    def get_tracks_by_ids(self, track_ids: List[str]) -> List[Track]:
        access_token = self.access_token_repository.get_access_token()

        response = requests.get(
            "https://api.spotify.com/v1/tracks",
            headers={"Authorization": f"Bearer {access_token}"},
            params={
                "ids": ",".join(track_ids),
            },
        )

        if response.status_code != requests.codes.ok:
            self.logger.error(
                f"cannot fetch tracks by ids correctly: {response.json()}"
            )

        items = response.json()["tracks"]
        features = self._get_features_by_ids(track_ids)

        tracks = [
            Track(
                spotify_id=item["id"],
                song_name=item["name"],
                album_name=item["album"]["name"],
                artist=item["artists"][0]["name"],
                bpm=features[idx]["tempo"],
                key=features[idx]["key"],
                mode=features[idx]["mode"],
                image_url=item["album"]["images"][0]["url"],
                preview_url=item["preview_url"],
                danceability=features[idx]["danceability"],
                energy=features[idx]["energy"],
            )
            for idx, item in enumerate(items)
        ]

        return tracks

    def get_tracks_by_query(self, query: str) -> List[Track]:
        access_token = self.access_token_repository.get_access_token()

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
        features = self._get_features_by_ids(ids)

        tracks = [
            Track(
                spotify_id=item["id"],
                song_name=item["name"],
                album_name=item["album"]["name"],
                artist=item["artists"][0]["name"],
                bpm=features[idx]["tempo"],
                key=features[idx]["key"],
                mode=features[idx]["mode"],
                image_url=item["album"]["images"][0]["url"],
                preview_url=item["preview_url"],
                danceability=features[idx]["danceability"],
                energy=features[idx]["energy"],
            )
            for idx, item in enumerate(items)
        ]

        return tracks
