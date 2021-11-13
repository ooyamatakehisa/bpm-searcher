from logging import Logger
from typing import List, Optional

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

    def _get_feature_by_id(
        self,
        spotify_id: str,
        access_token: str = None
    ) -> Optional[dict]:

        if access_token is None:
            access_token = self.access_token_repository.get_access_token()

        response = requests.get(
            f"https://api.spotify.com/v1/audio-features/{spotify_id}",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        body = response.json()

        # When the specified spotify id does not exist
        if response.status_code == requests.codes.bad_request:
            message = f"Specified spotify_id({spotify_id}) is invalid: {body}"
            self.logger.warning(message)
            return None

        elif response.status_code != requests.codes.ok:
            message = f"cannot fetch search a result feature correctly: {body}"
            self.logger.error(message)
            raise RuntimeError(message)

        return body

    def _get_features_by_ids(
        self,
        ids: List[str],
        access_token: str = None,
    ) -> List[Optional[dict]]:

        if access_token is None:
            access_token = self.access_token_repository.get_access_token()

        response = requests.get(
            "https://api.spotify.com/v1/audio-features",
            headers={"Authorization": f"Bearer {access_token}"},
            params={
                "ids": ",".join(ids),
            },
        )
        body = response.json()

        # When the specified spotify ids contain invalid one like including "_"
        if response.status_code == requests.codes.bad_request:
            message = f"Specified spotify_ids include invalid one: {body}"
            self.logger.warning(message)
            return []

        elif response.status_code != requests.codes.ok:
            message = f"cannot fetch search result features correctly: {body}"
            self.logger.error(message)
            raise RuntimeError(message)

        # None is returned for a spotify id that does not exist in spotify
        features = body["audio_features"]
        return features

    def get_track_by_id(self, track_id: str) -> Optional[Track]:
        spotify_id = track_id
        access_token = self.access_token_repository.get_access_token()

        response = requests.get(
            f"https://api.spotify.com/v1/tracks/{spotify_id}",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        body = response.json()

        # When the specified spotify id does not exist
        if response.status_code == requests.codes.bad_request:
            message = f"Specified spotify_id({spotify_id}) is invalid: {body}"
            self.logger.warning(message)
            return None

        elif response.status_code != requests.codes.ok:
            message = f"cannot fetch a track by id correctly: {body}"
            self.logger.error(message)
            raise RuntimeError(message)

        feature = self._get_feature_by_id(spotify_id)

        return Track(
            spotify_id=body["id"],
            song_name=body["name"],
            album_name=body["album"]["name"],
            artist=body["artists"][0]["name"],
            bpm=feature["tempo"],
            key=feature["key"],
            mode=feature["mode"],
            image_url=body["album"]["images"][0]["url"],
            preview_url=body["preview_url"],
            danceability=feature["danceability"],
            energy=feature["energy"],
        )

    def get_tracks_by_ids(self, track_ids: List[str]) -> List[Optional[Track]]:
        access_token = self.access_token_repository.get_access_token()

        response = requests.get(
            "https://api.spotify.com/v1/tracks",
            headers={"Authorization": f"Bearer {access_token}"},
            params={
                "ids": ",".join(track_ids),
            },
        )
        body = response.json()

        # When the specified spotify ids contain invalid one like including "_"
        if response.status_code == requests.codes.bad_request:
            message = f"Specified spotify_ids include invalid one: {body}"
            self.logger.warning(message)
            return []

        elif response.status_code != requests.codes.ok:
            message = f"cannot fetch tracks by ids correctly: {body}"
            self.logger.error(message)
            raise RuntimeError(message)

        # None is returned for a spotify id that does not exist in spotify
        items = body["tracks"]
        features = self._get_features_by_ids(track_ids)

        tracks = []
        for idx, item in enumerate(items):
            if item is None:
                track = None
            else:
                track = Track(
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
            tracks.append(track)

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
        body = response.json()

        if response.status_code != requests.codes.ok:
            message = f"cannot fetch search results correctly: {body}"
            self.logger.error(message)
            raise RuntimeError(message)

        items = body["tracks"]["items"]
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
