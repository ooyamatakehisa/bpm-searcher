import time
import unittest
from unittest import mock

from envs import Envs
from interactor.access_token_interactor import AccessTokenInteractor


class TestAccessTokenInteractor(unittest.TestCase):
    def create(self, access_token: str, ttl: float) -> None:
        self.access_token = access_token
        self.ttl = ttl

    def setUp(self) -> None:
        self.access_token_repostory = mock.MagicMock()
        self.access_token_repostory.create = self.create
        self.logger = mock.MagicMock()
        self.envs = Envs()
        return super().setUp()

    def test_get_access_token1(self) -> None:
        """
        The testcase where access_token is not stored in redis.
        """
        self.access_token_repostory.exist = lambda: False
        self.access_token_repostory.get = lambda: self.access_token
        self.access_token_repostory.get_ttl = lambda: self.ttl

        self.access_token = ""
        self.ttl = 100.0

        access_token_interactor = AccessTokenInteractor(
            self.envs,
            self.access_token_repostory,
            self.logger,
        )
        access_token = access_token_interactor.get_access_token()
        self.assertIsInstance(access_token, str)
        self.assertNotEqual(access_token, "")
        self.assertNotEqual(self.access_token, "")
        self.assertNotEqual(self.ttl, 100.0)

    def test_get_access_token2(self) -> None:
        """
        The testcase where the access_token is stored in redis,
        and the ttl is not expired.
        """
        self.access_token_repostory.exist = lambda: False
        self.access_token_repostory.get = lambda: self.access_token
        self.access_token_repostory.get_ttl = lambda: self.ttl

        access_token_interactor = AccessTokenInteractor(
            self.envs,
            self.access_token_repostory,
            self.logger,
        )
        access_token = access_token_interactor.get_access_token()

        self.access_token_repostory.exist = lambda: True
        self.access_token_repostory.get = lambda: self.access_token
        self.access_token_repostory.get_ttl = lambda: self.ttl

        # set ttl 10 minutes
        ttl = time.time() + 60 * 10
        self.ttl = ttl

        access_token_interactor = AccessTokenInteractor(
            self.envs,
            self.access_token_repostory,
            self.logger,
        )
        new_access_token = access_token_interactor.get_access_token()

        # check if ttl is not modified
        self.assertEqual(self.ttl, ttl)
        self.assertEqual(new_access_token, access_token)

    def test_get_access_token3(self) -> None:
        """
        The testcase where the access_token is stored in redis,
        but the ttl has expired.
        """
        self.access_token_repostory.exist = lambda: False
        self.access_token_repostory.get = lambda: self.access_token
        self.access_token_repostory.get_ttl = lambda: self.ttl

        access_token_interactor = AccessTokenInteractor(
            self.envs,
            self.access_token_repostory,
            self.logger,
        )
        access_token = access_token_interactor.get_access_token()

        self.access_token_repostory.exist = lambda: True
        self.access_token_repostory.get = lambda: self.access_token
        self.access_token_repostory.get_ttl = lambda: self.ttl

        # set ttl now
        ttl = time.time()
        self.ttl = ttl

        access_token_interactor = AccessTokenInteractor(
            self.envs,
            self.access_token_repostory,
            self.logger,
        )
        new_access_token = access_token_interactor.get_access_token()

        # check if ttl is modified
        self.assertNotEqual(self.ttl, ttl)
        self.assertNotEqual(new_access_token, access_token)


if __name__ == '__main__':
    unittest.main()
