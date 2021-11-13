from datetime import datetime
import unittest
from unittest import mock

from domain.model.track import PlaylistTrack, Track
from persistence.model import db
from persistence.model.user_playlist import UserPlaylistDataModel
from persistence.model.playlist import PlaylistInfoDataModel
from persistence.model.playlist_track import PlaylistTrackDataModel
from persistence.playlist import PlaylistRepositoryImpl
from persistence.track import TrackRepositoryImpl
from db.flask_sqlalchemy_testcase import MyTest


class TestTrackRepositoryImpl(MyTest):

    def setUp(self) -> None:
        self.logger = mock.MagicMock()
        self.db = db
        self.track_repository = mock.create_autospec(TrackRepositoryImpl, instance=True)
        self.track_repository.get_track_by_id.return_value = \
            mock.create_autospec(Track, instance=True)
        self.playlist_repository = PlaylistRepositoryImpl(
            self.db,
            logger=self.logger,
            track_repository=self.track_repository,
        )
        return super().setUp()

    def test_get_playlist1(self) -> None:
        """Testcase where the specified playlist exists
        """
        playlist_id = "playlist_id"
        playlist_info_data = PlaylistInfoDataModel(
            id=playlist_id,
            name="name",
            desc="desc",
            image_url="image_url",
            num_tracks=1,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        user_playlist_data = UserPlaylistDataModel(
            playlist_id=playlist_id,
            uid="uid",
        )
        playlist_track_data = PlaylistTrackDataModel(
            id="playlist_track_id",
            playlist_id=playlist_id,
            spotify_id="spotify_id1",
            order=1,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        self.db.session.add(playlist_info_data)
        self.db.session.add(user_playlist_data)
        self.db.session.add(playlist_track_data)
        self.db.session.commit()

        playlist = self.playlist_repository.get_playlist(playlist_id)
        self.assertEqual(playlist.playlist_info.num_tracks, 1)
        self.assertEqual(playlist.playlist_info.id, playlist_id)
        self.assertEqual(playlist.playlist_tracks[0].id, "playlist_track_id")
        self.assertEqual(playlist.playlist_tracks[0].order, 1)

    def test_get_playlist2(self) -> None:
        """Testcase where the specified playlist exists and no track exists
        """
        playlist_id = "playlist_id"
        playlist_info_data = PlaylistInfoDataModel(
            id=playlist_id,
            name="name",
            desc="desc",
            image_url="image_url",
            num_tracks=1,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        user_playlist_data = UserPlaylistDataModel(
            playlist_id=playlist_id,
            uid="uid",
        )
        self.db.session.add(playlist_info_data)
        self.db.session.add(user_playlist_data)
        self.db.session.commit()

        playlist = self.playlist_repository.get_playlist(playlist_id)
        self.assertEqual(playlist.playlist_info.num_tracks, 1)
        self.assertEqual(playlist.playlist_info.id, playlist_id)
        self.assertEqual(len(playlist.playlist_tracks), 0)

    def test_get_playlist3(self) -> None:
        """Testcase where the specified playlist does not exist
        """
        playlist = self.playlist_repository.get_playlist("playlist_id")
        self.assertEqual(playlist, None)

    def test_get_playlist_info1(self) -> None:
        """Testcase where the specified playlist exists in a DB
        """
        playlist_id = "playlist_id"
        playlist_info_data = PlaylistInfoDataModel(
            id=playlist_id,
            name="name",
            desc="desc",
            image_url="image_url",
            num_tracks=0,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        user_playlist_data = UserPlaylistDataModel(
            playlist_id=playlist_id,
            uid="uid",
        )
        self.db.session.add(playlist_info_data)
        self.db.session.add(user_playlist_data)
        self.db.session.commit()

        playlist_info = self.playlist_repository.get_playlist_info(playlist_id)
        self.assertEqual(playlist_info.id, playlist_id)
        self.assertEqual(playlist_info.name, "name")
        self.assertEqual(playlist_info.uid, "uid")

    def test_get_playlist_info2(self) -> None:
        """Testcase where the specified playlist does not exist in a DB
        """
        playlist_info = self.playlist_repository.get_playlist_info("playlist_id")
        self.assertEqual(playlist_info, None)

    def test_get_playlist_infos1(self) -> None:
        uid = "uid"
        playlist_info_data1 = PlaylistInfoDataModel(
            id="playlist_id1",
            name="name1",
            desc="desc2",
            image_url="image_url",
            num_tracks=0,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        user_playlist_data1 = UserPlaylistDataModel(
            playlist_id="playlist_id1",
            uid=uid,
        )
        playlist_info_data2 = PlaylistInfoDataModel(
            id="playlist_id2",
            name="name2",
            desc="desc2",
            image_url="image_url",
            num_tracks=1,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        user_playlist_data2 = UserPlaylistDataModel(
            playlist_id="playlist_id2",
            uid=uid,
        )
        self.db.session.add(playlist_info_data1)
        self.db.session.add(playlist_info_data2)
        self.db.session.add(user_playlist_data1)
        self.db.session.add(user_playlist_data2)
        self.db.session.commit()

        playlist_infos = self.playlist_repository.get_playlist_infos(uid)
        self.assertIsInstance(playlist_infos, list)
        self.assertEqual(len(playlist_infos), 2)
        self.assertEqual(playlist_infos[0].id, "playlist_id1")
        self.assertEqual(playlist_infos[1].id, "playlist_id2")
        self.assertEqual(playlist_infos[0].uid, uid)
        self.assertEqual(playlist_infos[1].uid, uid)

    def test_get_playlist_infos2(self) -> None:
        playlist_infos = self.playlist_repository.get_playlist_infos("uid")
        self.assertEqual(len(playlist_infos), 0)

    def test_get_playlist_track1(self) -> None:
        playlist_track_id = "playlist_track_id"
        playlist_track_data = PlaylistTrackDataModel(
            id=playlist_track_id,
            playlist_id="playlist_id",
            spotify_id="spotify_id",
            order=1,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        self.db.session.add(playlist_track_data)
        self.db.session.commit()

        playlist_track = self.playlist_repository.get_playlist_track(playlist_track_id)
        self.assertEqual(playlist_track.id, playlist_track_id)
        self.assertEqual(playlist_track.order, 1)
        self.assertIsInstance(playlist_track, PlaylistTrack)
        self.assertIsInstance(playlist_track.track, Track)

    def test_get_playlist_track2(self) -> None:
        playlist_track = self.playlist_repository.get_playlist_track("id")
        self.assertEqual(playlist_track, None)


if __name__ == '__main__':
    unittest.main()
