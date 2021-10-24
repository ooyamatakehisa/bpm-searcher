import unittest
from unittest import mock

from interactor.track_interactor import TrackInteractor

class TestTrackInteractor(unittest.TestCase):
    def create(self, access_token: str, ttl: float) -> None:
        self.access_token = access_token
        self.ttl = ttl

    def setUp(self) -> None:
        logger = mock.MagicMock()
        self.track_repository = mock.MagicMock()
        self.track_repository.get_tracks_by_query = lambda q: [q]
        self.track_interactor = TrackInteractor(
            self.track_repository,
        )
        return super().setUp()

    def test_get_tracks_by_query(self) -> None:
        query = "query"
        tracks = self.track_interactor.get_tracks_by_query(query)
        self.assertListEqual(tracks, [query])


if __name__ == '__main__':
    unittest.main()
