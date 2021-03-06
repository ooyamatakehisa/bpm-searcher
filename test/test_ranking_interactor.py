import time
import unittest
from unittest import mock

import fakeredis

from envs import Envs
from interactor.ranking_interactor import RankingInteractor
from persistence.access_token import AccessTokenRepositoryImpl


class TestRankingInteractor(unittest.TestCase):
    def create(self, ranking: list, ttl: float) -> None:
        self.ranking = ranking
        self.ttl = ttl

    def setUp(self) -> None:
        self.logger = mock.MagicMock()
        self.redis = fakeredis.FakeRedis(decode_responses=True)
        self.envs = Envs()
        self.access_token_repository = AccessTokenRepositoryImpl(
            envs=self.envs,
            logger=self.logger,
            redis=self.redis,
        )
        self.ranking_repostory = mock.MagicMock()
        self.ranking_repostory.create = self.create
        return super().setUp()

    def test_get_ranking1(self) -> None:
        """
        The testcase where ranking is not stored in redis.
        """
        self.ranking_repostory.exist = lambda: False
        self.ranking_repostory.get = lambda: self.ranking
        self.ranking_repostory.get_ttl = lambda: self.ttl

        self.ranking = []
        self.ttl = 100.0

        ranking_interactor = RankingInteractor(
            self.envs,
            self.access_token_repository,
            self.ranking_repostory,
            self.logger,
        )
        ranking = ranking_interactor.get_ranking()
        self.assertIsInstance(ranking, list)
        self.assertNotEqual(ranking, [])
        self.assertNotEqual(self.ranking, [])
        self.assertNotEqual(self.ttl, 100.0)

    def test_get_ranking2(self) -> None:
        """
        The testcase where the ranking is stored in redis,
        and the ttl is not expired.
        """
        self.ranking_repostory.exist = lambda: False
        self.ranking_repostory.get = lambda: self.ranking
        self.ranking_repostory.get_ttl = lambda: self.ttl

        ranking_interactor = RankingInteractor(
            self.envs,
            self.access_token_repository,
            self.ranking_repostory,
            self.logger,
        )
        ranking = ranking_interactor.get_ranking()

        self.ranking_repostory.exist = lambda: True
        self.ranking_repostory.get = lambda: self.ranking
        self.ranking_repostory.get_ttl = lambda: self.ttl

        # set ttl 10 minutes
        ttl = time.time() + 60 * 10
        self.ttl = ttl

        ranking_interactor = RankingInteractor(
            self.envs,
            self.access_token_repository,
            self.ranking_repostory,
            self.logger,
        )
        new_ranking = ranking_interactor.get_ranking()

        # check if ttl is not modified
        self.assertEqual(self.ttl, ttl)
        self.assertListEqual(new_ranking, ranking)

    def test_get_ranking3(self) -> None:
        """
        The testcase where the ranking is stored in redis,
        but the ttl has expired.
        """
        self.ranking_repostory.exist = lambda: False
        self.ranking_repostory.get = lambda: self.ranking
        self.ranking_repostory.get_ttl = lambda: self.ttl

        ranking_interactor = RankingInteractor(
            self.envs,
            self.access_token_repository,
            self.ranking_repostory,
            self.logger,
        )
        ranking_interactor.get_ranking()

        self.ranking_repostory.exist = lambda: True
        self.ranking_repostory.get = lambda: self.ranking
        self.ranking_repostory.get_ttl = lambda: self.ttl

        # set ttl now
        ttl = time.time()
        self.ttl = ttl

        ranking_interactor = RankingInteractor(
            self.envs,
            self.access_token_repository,
            self.ranking_repostory,
            self.logger,
        )
        ranking_interactor.get_ranking()

        # check if ttl is modified
        self.assertNotEqual(self.ttl, ttl)


if __name__ == '__main__':
    unittest.main()
