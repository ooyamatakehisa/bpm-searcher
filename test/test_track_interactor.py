import unittest
from unittest import mock

from envs import Envs
from interactor.track_interactor import TrackInteractor
from interactor.access_token_interactor import AccessTokenInteractor


class TestTrackInteractor(unittest.TestCase):
    def create(self, access_token: str, ttl: float) -> None:
        self.access_token = access_token
        self.ttl = ttl

    def setUp(self) -> None:
        access_token_repostory = mock.MagicMock()
        access_token_repostory.create = self.create
        access_token_repostory.exist = lambda: False
        access_token_repostory.get = lambda: self.access_token
        access_token_repostory.get_ttl = lambda: self.ttl
        logger = mock.MagicMock()
        access_token_usecase = AccessTokenInteractor(
            Envs(),
            access_token_repostory,
            logger,
        )
        self.track_interactor = TrackInteractor(
            Envs(),
            access_token_usecase,
            logger,
        )
        return super().setUp()

    def test_get_tracks1(self) -> None:
        """
        The testcase for beat it (micheal jackson).
        """
        res = self.track_interactor.get_tracks_by_query("Beat it")[0]
        expected = {
            "album_name": "Thriller 25 Super Deluxe Edition",
            "artist": "Michael Jackson",
            "bpm": 138.858,
            "danceability": 0.779,
            "energy": 0.867,
            "image_url": (
                "https://i.scdn.co/image/ab67616d0000b2734121faee8df82c526cbab2be"
            ),
            "key": 3,
            "mode": 0,
            "preview_url": (
                "https://p.scdn.co/mp3-preview/4901df6e0f8bf6ce93e08df7d98a50e220c45799"
                "?cid=12f045556f09486ba2ca641e0f062fa0"
            ),
            "song_name": "Beat It",
            "spotify_id": "1OOtq8tRnDM8kG2gqUPjAj"
        }
        self.assertDictEqual(res, expected)

    def test_get_tracks2(self) -> None:
        """
        The testcase for no results.
        """
        res = self.track_interactor.get_tracks_by_query("jreoafn rnegneogoe hilb")
        expected = []
        self.assertListEqual(res, expected)


if __name__ == '__main__':
    unittest.main()
