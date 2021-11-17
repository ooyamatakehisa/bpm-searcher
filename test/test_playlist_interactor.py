from datetime import datetime
import unittest
from unittest import mock

from interactor.playlist_interactor import PlaylistInteractor
from domain.model.playlist import Playlist, PlaylistInfo
from domain.model.track import PlaylistTrack, Track
from persistence.playlist import PlaylistRepositoryImpl


class TestPlaylistInteractor(unittest.TestCase):
    def setUp(self) -> None:
        playlist_repository = mock.create_autospec(
            PlaylistRepositoryImpl,
            instance=True,
        )
        self.playlist_interactor = PlaylistInteractor(
            logger=mock.MagicMock(),
            playlist_repository=playlist_repository,
            track_repository=mock.MagicMock(),
        )
        return super().setUp()

    def test_create_playlist(self) -> None:
        playlist_info = self.playlist_interactor.create_playlist(
            name="name",
            desc="desc",
            uid="uid",
        )
        self.assertIsInstance(playlist_info, PlaylistInfo)

    def test_get_playlist1(self) -> None:
        """Testcase where the playlist with the specified playlist_id exits
        """
        playlist_id = "playlist_id"
        self.playlist_interactor.playlist_repository.get_playlist \
            .return_value = mock.create_autospec(Playlist, instance=True)

        playlist = self.playlist_interactor.get_playlist(playlist_id)
        self.assertIsInstance(playlist, Playlist)

    def test_get_playlist2(self) -> None:
        """Testcase where the playlist with the specified playlist_id does not exist
        """
        playlist_id = "playlist_id"
        self.playlist_interactor.playlist_repository.get_playlist.return_value = None

        playlist = self.playlist_interactor.get_playlist(playlist_id)
        self.assertEqual(playlist, None)

    def test_get_playlist_infos(self) -> None:
        uid = "user id"
        playlist_info = mock.create_autospec(PlaylistInfo, instance=True)
        self.playlist_interactor.playlist_repository.get_playlist_infos \
            .return_value = [playlist_info]

        playlist_infos = self.playlist_interactor.get_playlist_infos(uid)
        self.assertIsInstance(playlist_infos, list)
        self.assertIsInstance(playlist_infos[0], PlaylistInfo)

    def test_delete_playlist1(self) -> None:
        expected_playlist_info = mock.create_autospec(PlaylistInfo, instance=True)
        self.playlist_interactor.playlist_repository.get_playlist_info \
            .return_value = expected_playlist_info

        actual_playlist_info = self.playlist_interactor.delete_playlist("playlist_id")
        self.assertEqual(actual_playlist_info, expected_playlist_info)

    def test_delete_playlist2(self) -> None:
        self.playlist_interactor.playlist_repository.get_playlist_info \
            .return_value = None

        actual_playlist_info = self.playlist_interactor.delete_playlist("playlist_id")
        self.assertEqual(actual_playlist_info, None)

    def test_delete_track1(self) -> None:
        """Testcase where specified playlist and playlist track exists
        """
        playlist_id = "playlist_id1"
        playlist_track_id1 = "playlist_track_id1"
        playlist_track1 = PlaylistTrack(
            id=playlist_track_id1,
            order=1,
            track=Track(
                spotify_id="spotify_id1",
                song_name="song_name1",
                artist="artist1",
                album_name="album_name1",
                bpm=111.1,
                danceability=111.1,
                energy=111.1,
                image_url="image_url1",
                key=1,
                mode=1,
                preview_url="preview_url1",
            ),
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        playlist_track2 = PlaylistTrack(
            id="playlist_track_id2",
            order=2,
            track=Track(
                spotify_id="spotify_id2",
                song_name="song_name2",
                artist="artist2",
                album_name="album_name2",
                bpm=222.2,
                danceability=222.2,
                energy=222.2,
                image_url="image_url2",
                key=2,
                mode=2,
                preview_url="preview_url2",
            ),
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        self.playlist_interactor.playlist_repository.get_playlist \
            .return_value = Playlist(
                playlist_info=PlaylistInfo(
                    id=playlist_id,
                    uid="userid",
                    name="name",
                    desc="desc",
                    num_tracks=2,
                    image_url="image_url",
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                ),
                playlist_tracks=[
                    playlist_track1,
                    playlist_track2,
                ],
            )
        self.playlist_interactor.playlist_repository.get_playlist_track \
            .return_value = playlist_track1

        actual_playlist = self.playlist_interactor.delete_track(
            playlist_id,
            playlist_track_id1,
        )
        self.assertIsInstance(actual_playlist, Playlist)

    def test_delete_track2(self) -> None:
        """Testcase where specified playlist exists but playlist track does not
        """
        playlist_id = "playlist_id1"
        playlist_track_id1 = "playlist_track_id1"
        self.playlist_interactor.playlist_repository.get_playlist \
            .return_value = mock.create_autospec(Playlist, instance=True)
        self.playlist_interactor.playlist_repository.get_playlist_track \
            .return_value = None

        actual_playlist = self.playlist_interactor.delete_track(
            playlist_id,
            playlist_track_id1,
        )
        self.assertEqual(actual_playlist, None)

    def test_delete_track3(self) -> None:
        """Testcase where specified playlist does not exist but playlist exists
        """
        playlist_id = "playlist_id1"
        playlist_track_id1 = "playlist_track_id1"
        self.playlist_interactor.playlist_repository.get_playlist \
            .return_value = None
        self.playlist_interactor.playlist_repository.get_playlist_track \
            .return_value = mock.create_autospec(PlaylistTrack, instance=True)

        actual_playlist = self.playlist_interactor.delete_track(
            playlist_id,
            playlist_track_id1,
        )
        self.assertEqual(actual_playlist, None)

    def test_update_playlist1(self) -> None:
        """Testcase where kind is "info" and specified playlist exists
        """
        self.playlist_interactor.playlist_repository.get_playlist_info \
            .return_value = mock.MagicMock()

        playlist_info = self.playlist_interactor.update_playlist(
            kind="info",
            playlist_id="playlist_id",
            name="name",
            desc="desc",
        )
        self.assertIsInstance(playlist_info, PlaylistInfo)

    def test_update_playlist2(self) -> None:
        """Testcase where kind is "info" and specified playlist does not exists
        """
        self.playlist_interactor.playlist_repository.get_playlist_info \
            .return_value = None

        playlist_info = self.playlist_interactor.update_playlist(
            kind="info",
            playlist_id="playlist_id",
            name="name",
            desc="desc",
        )
        self.assertEqual(playlist_info, None)

    def test_update_playlist3(self) -> None:
        """Testcase where kind is "track" and specified playlist exists
        """
        self.playlist_interactor.playlist_repository.get_playlist \
            .return_value = Playlist(
                playlist_info=PlaylistInfo(
                    id="playlist_id",
                    uid="userid",
                    name="name",
                    desc="desc",
                    num_tracks=0,
                    image_url="image_url",
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                ),
                playlist_tracks=[],
            )
        self.playlist_interactor.track_repository.get_track_by_id \
            .return_value = Track(
                spotify_id="spotify_id1",
                song_name="song_name1",
                artist="artist1",
                album_name="album_name1",
                bpm=111.1,
                danceability=111.1,
                energy=111.1,
                image_url="image_url1",
                key=1,
                mode=1,
                preview_url="preview_url1",
            )

        playlist = self.playlist_interactor.update_playlist(
            kind="track",
            playlist_id="playlist_id",
            spotify_id="spotify_id",
        )
        self.assertIsInstance(playlist, Playlist)

    def test_update_playlist4(self) -> None:
        """Testcase where kind is "track" and specified playlist does not exist
        """
        self.playlist_interactor.playlist_repository.get_playlist \
            .return_value = None
        self.playlist_interactor.track_repository.get_track_by_id \
            .return_value = mock.create_autospec(Track, instance=True)

        playlist = self.playlist_interactor.update_playlist(
            kind="track",
            playlist_id="playlist_id",
            spotify_id="spotify_id",
        )
        self.assertEqual(playlist, None)

    def test_update_playlist5(self) -> None:
        """Testcase where kind is "track" and specified playlist_track does not exist
        """
        self.playlist_interactor.playlist_repository.get_playlist \
            .return_value = Playlist(
                playlist_info=PlaylistInfo(
                    id="playlist_id",
                    uid="userid",
                    name="name",
                    desc="desc",
                    num_tracks=0,
                    image_url="image_url",
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                ),
                playlist_tracks=[],
            )
        self.playlist_interactor.track_repository.get_track_by_id \
            .return_value = None

        playlist = self.playlist_interactor.update_playlist(
            kind="track",
            playlist_id="playlist_id",
            spotify_id="spotify_id",
        )
        self.assertEqual(playlist, None)


if __name__ == '__main__':
    unittest.main()
