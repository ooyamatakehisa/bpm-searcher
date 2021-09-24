import unittest

import fakeredis

from persistence.access_token import AccessTokenRepositoryImpl


class TestAccessTokenRepository(unittest.TestCase):
    def setUp(self) -> None:
        self.redis = fakeredis.FakeRedis(decode_responses=True)
        self.access_token_persistence = AccessTokenRepositoryImpl(
            redis=self.redis
        )
        return super().setUp()

    def test_create(self) -> None:
        expected_access_token = "access_token_test"
        expected_ttl = 100
        self.access_token_persistence.create(
            access_token=expected_access_token,
            ttl=expected_ttl,
        )
        actual_access_token = self.redis.hget("access_token", "access_token")
        actual_ttl = float(self.redis.hget("access_token", "ttl"))
        self.assertEqual(actual_access_token, expected_access_token)
        self.assertEqual(actual_ttl, expected_ttl)

    def test_exist1(self) -> None:
        res = self.access_token_persistence.exist()
        self.assertFalse(res)

    def test_exist2(self) -> None:
        self.access_token_persistence.create(
            access_token="access_token",
            ttl=100,
        )
        res = self.access_token_persistence.exist()
        self.assertTrue(res)

    def test_get(self):
        expected_access_token = "access_token_test"
        self.access_token_persistence.create(
            access_token=expected_access_token,
            ttl=100,
        )
        actual_access_token = self.access_token_persistence.get()
        self.assertEqual(actual_access_token, expected_access_token)

    def test_get_ttl(self):
        expected_ttl = 100
        self.access_token_persistence.create(
            access_token="access_token",
            ttl=expected_ttl,
        )
        actual_ttl = self.access_token_persistence.get_ttl()
        self.assertEqual(actual_ttl, expected_ttl)
