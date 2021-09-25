import unittest
from unittest.mock import MagicMock

from flask import Flask

from controller.ranking_controller import RankingController


class TestRankingController(unittest.TestCase):
    def setUp(self) -> None:
        self.app = Flask(__name__)
        return super().setUp()

    def test_get_ranking(self):
        expected_ranking = [
            {"song": "song_name", "artist": "artist1"},
            {"song": "song_name2", "artist": "artist2"},
            {"song": "song_name3", "artist": "artist3"},
        ]
        ranking_interactor = MagicMock()
        ranking_interactor.get_ranking = lambda: expected_ranking
        ranking_controller = RankingController(
            ranking_usecase=ranking_interactor
        )
        self.app.add_url_rule(
            rule="/api/v1/ranking",
            view_func=ranking_controller.get_ranking
        )
        with self.app.test_client() as c:
            rv = c.get("/api/v1/ranking")
            actual_ranking = rv.get_json()
            self.assertListEqual(actual_ranking, expected_ranking)


if __name__ == '__main__':
    unittest.main()
