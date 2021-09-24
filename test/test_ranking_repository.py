import json
import unittest

import fakeredis

from persistence.ranking import RankingRepositoryImpl


class TestRankingRepository(unittest.TestCase):
    def setUp(self) -> None:
        self.redis = fakeredis.FakeRedis(decode_responses=True)
        self.ranking_persistence = RankingRepositoryImpl(
            redis=self.redis
        )
        self.ranking = [
            {
                "album_name": "F*CK LOVE 3: OVER YOU",
                "artist": "The Kid LAROI",
                "bpm": 169.928,
                "danceability": 0.591,
                "energy": 0.764,
                "image_url": (
                    "https://i.scdn.co/image/ab67616d0000b2738e6551a2944764bc8e33a960"
                ),
                "key": 1,
                "mode": 1,
                "preview_url": (
                    "https://p.scdn.co/mp3-preview/"
                    "dd4d8d66b97b6edcb5358135e72620715e1449f9"
                    "?cid=12f045556f09486ba2ca641e0f062fa0"
                ),
                "song_name": "STAY (with Justin Bieber)",
                "spotify_id": "5PjdY0CKGZdEuoNab3yDmX"
            },
            {
                "album_name": "MONTERO",
                "artist": "Lil Nas X",
                "bpm": 150.087,
                "danceability": 0.741,
                "energy": 0.691,
                "image_url": (
                    "https://i.scdn.co/image/ab67616d0000b273be82673b5f79d9658ec0a9fd"
                ),
                "key": 10,
                "mode": 0,
                "preview_url": (
                    "https://p.scdn.co/mp3-preview/"
                    "c1cb40d748692992bd5e476fc17ffe16f31016e3"
                    "?cid=12f045556f09486ba2ca641e0f062fa0"
                ),
                "song_name": "INDUSTRY BABY (feat. Jack Harlow)",
                "spotify_id": "5Z9KJZvQzH6PFmb8SNkxuk"
            },
            {
                "album_name": "Dreamland (+ Bonus Levels)",
                "artist": "Glass Animals",
                "bpm": 80.87,
                "danceability": 0.761,
                "energy": 0.525,
                "image_url": (
                    "https://i.scdn.co/image/ab67616d0000b2739e495fb707973f3390850eea"
                ),
                "key": 11,
                "mode": 1,
                "preview_url": "null",
                "song_name": "Heat Waves",
                "spotify_id": "02MWAaffLxlfxAUY7c5dvx"
            },
            {
                "album_name": "MONTERO",
                "artist": "Lil Nas X",
                "bpm": 87.981,
                "danceability": 0.737,
                "energy": 0.846,
                "image_url": (
                    "https://i.scdn.co/image/ab67616d0000b273be82673b5f79d9658ec0a9fd"
                ),
                "key": 1,
                "mode": 0,
                "preview_url": (
                    "https://p.scdn.co/mp3-preview/"
                    "75aa4d781c96fe990214d04f4e61efb702bf635c"
                    "?cid=12f045556f09486ba2ca641e0f062fa0"
                ),
                "song_name": "THATS WHAT I WANT",
                "spotify_id": "0e8nrvls4Qqv5Rfa2UhqmO"
            },
        ]
        return super().setUp()

    def test_create(self) -> None:
        expected_ranking = self.ranking
        expected_ttl = 100
        self.ranking_persistence.create(
            ranking=expected_ranking,
            ttl=expected_ttl,
        )
        ranking_str = self.redis.hget("ranking", "ranking")
        actual_ranking = json.loads(ranking_str)
        actual_ttl = float(self.redis.hget("ranking", "ttl"))
        self.assertListEqual(actual_ranking, expected_ranking)
        self.assertEqual(actual_ttl, expected_ttl)

    def test_exist1(self) -> None:
        res = self.ranking_persistence.exist()
        self.assertFalse(res)

    def test_exist2(self) -> None:
        ranking = self.ranking
        self.ranking_persistence.create(
            ranking=ranking,
            ttl=100,
        )
        res = self.ranking_persistence.exist()
        self.assertTrue(res)

    def test_get(self):
        expected_ranking = self.ranking
        self.ranking_persistence.create(
            ranking=expected_ranking,
            ttl=100,
        )
        actual_ranking = self.ranking_persistence.get()
        self.assertListEqual(actual_ranking, expected_ranking)

    def test_get_ttl(self):
        ranking = self.ranking
        expected_ttl = 100
        self.ranking_persistence.create(
            ranking=ranking,
            ttl=expected_ttl,
        )
        actual_ttl = self.ranking_persistence.get_ttl()
        self.assertEqual(actual_ttl, expected_ttl)
