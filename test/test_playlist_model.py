from datetime import datetime
import unittest

from domain.model.playlist import Playlist, PlaylistInfo
from domain.model.track import PlaylistTrack, Track


class TestPlaylistInteractor(unittest.TestCase):

    def test_delete1(self) -> None:
        """Testcase where the playlist has 2 tracks and delete first track
        """
        playlist_id = "playlist_id1"
        playlist_track_id1 = "playlist_track_id1"
        date_time = datetime.now()
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
            created_at=date_time,
            updated_at=date_time,
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
            created_at=date_time,
            updated_at=date_time,
        )
        playlist = Playlist(
                playlist_info=PlaylistInfo(
                    id=playlist_id,
                    uid="userid",
                    name="name",
                    desc="desc",
                    num_tracks=2,
                    image_url="image_url1",
                    created_at=date_time,
                    updated_at=date_time,
                ),
                playlist_tracks=[
                    playlist_track1,
                    playlist_track2,
                ],
            )

        new_playlist = playlist.delete(playlist_track1)
        self.assertEqual(new_playlist.playlist_info.id, playlist_id)
        self.assertEqual(new_playlist.playlist_info.num_tracks, 1)
        self.assertEqual(new_playlist.playlist_info.image_url, "image_url2")
        self.assertEqual(len(new_playlist.playlist_tracks), 1)
        self.assertEqual(new_playlist.playlist_tracks[0].id, "playlist_track_id2")
        self.assertEqual(new_playlist.playlist_tracks[0].order, 1)

    def test_delete2(self) -> None:
        """Testcase where the playlist has 2 tracks and delete second track
        """
        playlist_id = "playlist_id1"
        playlist_track_id1 = "playlist_track_id1"
        date_time = datetime.now()
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
            created_at=date_time,
            updated_at=date_time,
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
            created_at=date_time,
            updated_at=date_time,
        )
        playlist = Playlist(
                playlist_info=PlaylistInfo(
                    id=playlist_id,
                    uid="userid",
                    name="name",
                    desc="desc",
                    num_tracks=2,
                    image_url="image_url1",
                    created_at=date_time,
                    updated_at=date_time,
                ),
                playlist_tracks=[
                    playlist_track1,
                    playlist_track2,
                ],
            )

        new_playlist = playlist.delete(playlist_track2)
        self.assertEqual(new_playlist.playlist_info.id, playlist_id)
        self.assertEqual(new_playlist.playlist_info.num_tracks, 1)
        self.assertEqual(new_playlist.playlist_info.image_url, "image_url1")
        self.assertEqual(len(new_playlist.playlist_tracks), 1)
        self.assertEqual(new_playlist.playlist_tracks[0].id, "playlist_track_id1")
        self.assertEqual(new_playlist.playlist_tracks[0].order, 1)

    def test_delete3(self) -> None:
        """Testcase where the playlist has 1 tracks and delete it
        """
        playlist_id = "playlist_id1"
        playlist_track_id1 = "playlist_track_id1"
        date_time = datetime.now()
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
            created_at=date_time,
            updated_at=date_time,
        )
        playlist = Playlist(
                playlist_info=PlaylistInfo(
                    id=playlist_id,
                    uid="userid",
                    name="name",
                    desc="desc",
                    num_tracks=1,
                    image_url="image_url1",
                    created_at=date_time,
                    updated_at=date_time,
                ),
                playlist_tracks=[
                    playlist_track1,
                ],
            )

        new_playlist = playlist.delete(playlist_track1)
        self.assertEqual(new_playlist.playlist_info.id, playlist_id)
        self.assertEqual(new_playlist.playlist_info.num_tracks, 0)
        self.assertEqual(new_playlist.playlist_info.image_url, None)
        self.assertEqual(len(new_playlist.playlist_tracks), 0)

    def test_add1(self) -> None:
        """Testcase where the playlist has 1 track and add a new track
        """
        playlist_id = "playlist_id1"
        playlist_track_id1 = "playlist_track_id1"
        date_time = datetime.now()
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
            created_at=date_time,
            updated_at=date_time,
        )
        new_track = Track(
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
        )
        playlist = Playlist(
            playlist_info=PlaylistInfo(
                id=playlist_id,
                uid="userid",
                name="name",
                desc="desc",
                num_tracks=1,
                image_url="image_url1",
                created_at=date_time,
                updated_at=date_time,
            ),
            playlist_tracks=[
                playlist_track1,
            ],
        )

        new_playlist = playlist.add(new_track)
        self.assertEqual(new_playlist.playlist_info.id, playlist_id)
        self.assertEqual(new_playlist.playlist_info.num_tracks, 2)
        self.assertEqual(new_playlist.playlist_info.image_url, "image_url1")
        self.assertEqual(len(new_playlist.playlist_tracks), 2)
        self.assertEqual(new_playlist.playlist_tracks[0].id, "playlist_track_id1")
        self.assertEqual(new_playlist.playlist_tracks[0].order, 1)
        self.assertEqual(new_playlist.playlist_tracks[1].order, 2)

    def test_add2(self) -> None:
        """Testcase where the playlist has no track and add a new track
        """
        playlist_id = "playlist_id1"
        date_time = datetime.now()
        new_track = Track(
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
        playlist = Playlist(
            playlist_info=PlaylistInfo(
                id=playlist_id,
                uid="userid",
                name="name",
                desc="desc",
                num_tracks=0,
                image_url="image_url1",
                created_at=date_time,
                updated_at=date_time,
            ),
            playlist_tracks=[],
        )

        new_playlist = playlist.add(new_track)
        self.assertEqual(new_playlist.playlist_info.id, playlist_id)
        self.assertEqual(new_playlist.playlist_info.num_tracks, 1)
        self.assertEqual(new_playlist.playlist_info.image_url, "image_url1")
        self.assertEqual(len(new_playlist.playlist_tracks), 1)
        self.assertEqual(new_playlist.playlist_tracks[0].order, 1)


if __name__ == '__main__':
    unittest.main()
