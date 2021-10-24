import time
import unittest
from unittest import mock

import fakeredis

from envs import Envs
from persistence.access_token import AccessTokenRepositoryImpl


class TestAccessTokenRepository(unittest.TestCase):
    def setUp(self) -> None:
        self.logger = mock.MagicMock()
        self.redis = fakeredis.FakeRedis(decode_responses=True)
        self.access_token_persistence = AccessTokenRepositoryImpl(
            envs=Envs(),
            logger=self.logger,
            redis=self.redis,
        )
        return super().setUp()

    def test_get_access_token1(self) -> None:
        """Testcase where no access token is stored in redis
        """
        access_token = self.access_token_persistence.get_access_token()
        access_token_redis = self.redis.hget("access_token", "access_token")
        self.assertEqual(access_token, access_token_redis)

    def test_get_access_token2(self) -> None:
        """Testcase where access token is stored in redis and ttl is not expired
        """
        expected_access_token = "access_token_test"
        expected_ttl = time.time() + 60 * 50
        self.redis.hset("access_token", "access_token", expected_access_token)
        self.redis.hset("access_token", "ttl", expected_ttl)

        actual_access_token = self.access_token_persistence.get_access_token()
        actual_ttl = float(self.redis.hget("access_token", "ttl"))
        self.assertEqual(actual_access_token, expected_access_token)
        self.assertEqual(actual_ttl, expected_ttl)

    def test_get_access_token3(self) -> None:
        """Testcase where access token is stored in redis and ttl is expired
        """
        access_token = "access_token_test"
        ttl = time.time()
        self.redis.hset("access_token", "access_token", access_token)
        self.redis.hset("access_token", "ttl", ttl)

        actual_access_token = self.access_token_persistence.get_access_token()
        actual_ttl = float(self.redis.hget("access_token", "ttl"))
        self.assertNotEqual(actual_access_token, access_token)
        self.assertNotEqual(actual_ttl, ttl)

    def test_get_access_token_from_cache(self) -> None:
        expected_access_token = "access_token_test"
        ttl = time.time()
        self.redis.hset("access_token", "access_token", expected_access_token)
        self.redis.hset("access_token", "ttl", ttl)
        actual_access_token = (
            self.access_token_persistence._get_access_token_from_cache()
        )
        self.assertEqual(actual_access_token, expected_access_token)

    def test_get_access_token_from_spotify(self) -> None:
        access_token = self.access_token_persistence._get_access_token_from_spotify()
        self.assertIsInstance(access_token, str)

    def test_save_cache(self) -> None:
        expected_access_token = "access_token_test"
        self.access_token_persistence._save_cache(expected_access_token)

        actual_access_token = self.redis.hget("access_token", "access_token")
        self.assertEqual(actual_access_token, expected_access_token)

    def test_valid_cache1(self) -> None:
        """Testcase where access token is not stored in redis
        """
        valid = self.access_token_persistence._valid_cache()
        self.assertIs(valid, False)

    def test_valid_cache2(self) -> None:
        """Testcase where access token is stored in redis and ttl is not expired
        """
        expected_access_token = "access_token_test"
        expected_ttl = time.time() + 60 * 50
        self.redis.hset("access_token", "access_token", expected_access_token)
        self.redis.hset("access_token", "ttl", expected_ttl)

        valid = self.access_token_persistence._valid_cache()
        self.assertIs(valid, True)

    def test_valid_cache3(self) -> None:
        """Testcase where access token is stored in redis and ttl is expired
        """
        access_token = "access_token_test"
        ttl = time.time()
        self.redis.hset("access_token", "access_token", access_token)
        self.redis.hset("access_token", "ttl", ttl)

        valid = self.access_token_persistence._valid_cache()
        self.assertIs(valid, False)
