import unittest
from unittest.mock import MagicMock

from flask import Flask

from controller.track_controller import TrackController


class TestTrackController(unittest.TestCase):
    def setUp(self) -> None:
        self.app = Flask(__name__)
        return super().setUp()

    def test_get_tracks1(self):
        expected_track = [
            {"song": "song_name", "artist": "artist1"},
            {"song": "song_name2", "artist": "artist2"},
            {"song": "song_name3", "artist": "artist3"},
        ]
        track_interactor = MagicMock()
        track_interactor.get_tracks_by_query = lambda q: expected_track
        track_controller = TrackController(
            track_usecase=track_interactor
        )
        self.app.add_url_rule(
            rule="/api/v1/track",
            view_func=track_controller.get_tracks
        )
        with self.app.test_client() as c:
            rv = c.get("/api/v1/track?search=test")
            actual_track = rv.get_json()
            self.assertListEqual(actual_track, expected_track)

    def test_get_tracks2(self):
        track_interactor = MagicMock()
        track_controller = TrackController(
            track_usecase=track_interactor
        )
        self.app.add_url_rule(
            rule="/api/v1/track",
            view_func=track_controller.get_tracks
        )
        expected_message = b"no search query"
        expected_status = 400
        with self.app.test_client() as c:
            rv = c.get("/api/v1/track?search=")
            actual_message = rv.data
            actual_response_code = rv.status_code
            self.assertEqual(actual_message, expected_message)
            self.assertEqual(actual_response_code, expected_status)

    def test_get_tracks3(self):
        track_interactor = MagicMock()
        track_interactor.get_tracks_by_query = lambda q: []
        track_controller = TrackController(
            track_usecase=track_interactor
        )
        self.app.add_url_rule(
            rule="/api/v1/track",
            view_func=track_controller.get_tracks
        )
        expected_message = b"no search result for the specified query"
        expected_status = 404
        with self.app.test_client() as c:
            rv = c.get("/api/v1/track?search=gtgegetge+grgege")
            actual_message = rv.data
            actual_response_code = rv.status_code
            self.assertEqual(actual_message, expected_message)
            self.assertEqual(actual_response_code, expected_status)


if __name__ == '__main__':
    unittest.main()
