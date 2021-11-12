import unittest
from unittest import mock

import fakeredis

from envs import Envs
from domain.model.track import Track
from persistence.access_token import AccessTokenRepositoryImpl
from persistence.track import TrackRepositoryImpl


class TestTrackRepositoryImpl(unittest.TestCase):
    def setUp(self) -> None:
        self.logger = mock.MagicMock()
        self.redis = fakeredis.FakeRedis(decode_responses=True)
        self.access_token_persistence = AccessTokenRepositoryImpl(
            envs=Envs(),
            logger=self.logger,
            redis=self.redis,
        )
        self.track_repository = TrackRepositoryImpl(
            self.logger,
            self.access_token_persistence,
        )
        return super().setUp()

    def test_get_feature_by_id1(self) -> None:
        """Testcase where access token is not specified"""
        spotify_id = "0gplL1WMoJ6iYaPgMCL0gX"
        feature = self.track_repository._get_feature_by_id(spotify_id)
        self.assertIsInstance(feature, dict)
        expected_bpm = 142
        actual_bpm = int(round(float(feature["tempo"])))
        self.assertEqual(actual_bpm, expected_bpm)

    def test_get_feature_by_id2(self) -> None:
        """Testcase where access token is specified"""
        spotify_id = "0gplL1WMoJ6iYaPgMCL0gX"
        access_token = self.access_token_persistence.get_access_token()
        feature = self.track_repository._get_feature_by_id(spotify_id, access_token)
        self.assertIsInstance(feature, dict)
        expected_bpm = 142
        actual_bpm = int(round(float(feature["tempo"])))
        self.assertEqual(actual_bpm, expected_bpm)

    def test_get_feature_by_id3(self) -> None:
        """Testcase where spotify id is invalid"""
        spotify_id = "invalid_spotify_id"
        access_token = self.access_token_persistence.get_access_token()
        feature = self.track_repository._get_feature_by_id(spotify_id, access_token)
        self.assertEqual(feature, None)

    def test_get_feature_by_id4(self) -> None:
        """Testcase where access token is invalid"""
        spotify_id = "0gplL1WMoJ6iYaPgMCL0gX"
        access_token = "invalid_access_token"
        with self.assertRaises(RuntimeError):
            self.track_repository._get_feature_by_id(spotify_id, access_token)

    def test_get_features_by_ids1(self) -> None:
        """Testcase where access token is not specified"""
        spotify_ids = ["0gplL1WMoJ6iYaPgMCL0gX"]
        features = self.track_repository._get_features_by_ids(spotify_ids)
        self.assertIsInstance(features, list)
        self.assertIsInstance(features[0], dict)
        expected_bpm = 142
        actual_bpm = int(round(float(features[0]["tempo"])))
        self.assertEqual(actual_bpm, expected_bpm)

    def test_get_features_by_ids2(self) -> None:
        """Testcase where access token is specified"""
        spotify_ids = ["0gplL1WMoJ6iYaPgMCL0gX"]
        access_token = self.access_token_persistence.get_access_token()
        features = self.track_repository._get_features_by_ids(
            spotify_ids,
            access_token,
        )
        self.assertIsInstance(features, list)
        self.assertIsInstance(features[0], dict)
        expected_bpm = 142
        actual_bpm = int(round(float(features[0]["tempo"])))
        self.assertEqual(actual_bpm, expected_bpm)

    def test_get_feature_by_ids3(self) -> None:
        """Testcase where spotify ids include a invalid id"""
        spotify_ids = ["0gplL1WMoJ6iYaPgMCL0gX", "invalid_spotify_id"]
        access_token = self.access_token_persistence.get_access_token()
        features = self.track_repository._get_features_by_ids(
            spotify_ids,
            access_token,
        )
        self.assertIsInstance(features, list)
        self.assertIsInstance(features[0], dict)
        self.assertEqual(features[1], None)
        expected_bpm = 142
        actual_bpm = int(round(float(features[0]["tempo"])))
        self.assertEqual(actual_bpm, expected_bpm)

    def test_get_feature_by_ids4(self) -> None:
        """Testcase where access token is invalid"""
        spotify_ids = ["0gplL1WMoJ6iYaPgMCL0gX"]
        access_token = "invalid_access_token"
        with self.assertRaises(RuntimeError):
            self.track_repository._get_features_by_ids(spotify_ids, access_token)

    def test_get_track_by_id1(self) -> None:
        """Testcase where　spotify id is valid"""
        spotify_id = "0gplL1WMoJ6iYaPgMCL0gX"
        track = self.track_repository.get_track_by_id(spotify_id)
        self.assertIsInstance(track, Track)
        self.assertEqual(track.spotify_id, spotify_id)

        expected_bpm = 142
        actual_bpm = int(round(float(track.bpm)))
        self.assertEqual(actual_bpm, expected_bpm)
        self.assertEqual(track.artist, "Adele")

    def test_get_track_by_id2(self) -> None:
        """Testcase where　spotify id is invalid"""
        spotify_id = "0gplL1WMoJ6iYaPgMCL0g"
        track = self.track_repository.get_track_by_id(spotify_id)
        self.assertEqual(track, None)

    def test_get_tracks_by_ids1(self) -> None:
        """Testcase where all spotify ids are valid"""
        spotify_ids = ["0gplL1WMoJ6iYaPgMCL0gX"]
        tracks = self.track_repository.get_tracks_by_ids(spotify_ids)
        self.assertEqual(len(tracks), 1)
        self.assertIsInstance(tracks, list)
        self.assertIsInstance(tracks[0], Track)
        self.assertEqual(tracks[0].spotify_id, spotify_ids[0])

        expected_bpm = 142
        actual_bpm = int(round(float(tracks[0].bpm)))
        self.assertEqual(actual_bpm, expected_bpm)
        self.assertEqual(tracks[0].artist, "Adele")

    def test_get_tracks_by_ids2(self) -> None:
        """Testcase where spotify ids include a invalid id"""
        spotify_ids = ["0gplL1WMoJ6iYaPgMCL0gX", "0gplL1WMoJ6iYaPgMCL0g"]
        tracks = self.track_repository.get_tracks_by_ids(spotify_ids)
        self.assertEqual(len(tracks), 2)
        self.assertIsInstance(tracks, list)
        self.assertIsInstance(tracks[0], Track)
        self.assertEqual(tracks[1], None)
        self.assertEqual(tracks[0].spotify_id, spotify_ids[0])

        expected_bpm = 142
        actual_bpm = int(round(float(tracks[0].bpm)))
        self.assertEqual(actual_bpm, expected_bpm)
        self.assertEqual(tracks[0].artist, "Adele")

    def test_get_tracks_by_query1(self) -> None:
        query = "adele easy on me"
        tracks = self.track_repository.get_tracks_by_query(query)
        self.assertIsInstance(tracks, list)
        self.assertIsInstance(tracks[0], Track)
        self.assertEqual(tracks[0].spotify_id, "0gplL1WMoJ6iYaPgMCL0gX")

        expected_bpm = 142
        actual_bpm = int(round(float(tracks[0].bpm)))
        self.assertEqual(actual_bpm, expected_bpm)
        self.assertEqual(tracks[0].artist, "Adele")

    def test_get_tracks_by_query2(self) -> None:
        query = "frafa jfeorj oreafo far"
        tracks = self.track_repository.get_tracks_by_query(query)
        self.assertIsInstance(tracks, list)
        self.assertEqual(len(tracks), 0)


if __name__ == '__main__':
    unittest.main()
