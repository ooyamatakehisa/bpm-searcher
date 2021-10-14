from abc import ABCMeta, abstractmethod
from typing import List

from domain.model.playlist import Playlist, PlaylistInfo
from domain.model.track import PlaylistTrack


class PlaylistRepository(metaclass=ABCMeta):
    @abstractmethod
    def get_playlist_infos(self, uid: str) -> List[PlaylistInfo]:
        pass

    @abstractmethod
    def get_playlist(playlist_id: str) -> Playlist:
        pass

    @abstractmethod
    def get_playlist_info(playlist_id: str) -> PlaylistInfo:
        """Get PlaylistInfo object of the playlist with specified playlist_id.
        PlaylistInfo include metadata of playlist such as name or descrption.

        Args:
            playlist_id (str): playlist id

        Returns:
            PlaylistInfo: PlaylistInfo object
        """
        pass

    @abstractmethod
    def get_playlist_tracks(playlist_id: str) -> List[PlaylistTrack]:
        """Get list of PlaylistTrack objects of the playlist with the specified playlist

        Args:
            playlist_id (str): [description]

        Returns:
            List[PlaylistTrack]: [description]
        """
        pass

    @abstractmethod
    def save_playlist(self, playlist_info: PlaylistInfo, spotify_id: str) -> None:
        """Add tracks to the given playlist. A track is represented as
        spotify_id and spotify_id is made relation to the playlist.
        This method does not affect playlist information such as a playlist name.

        Args:
            playlist_info (PlaylistInfo): PlaylistInfo object
            spotify_id (str): spotify_id of the track to be added
        """
        pass

    @abstractmethod
    def save_playlist_info(self, playlist_info: PlaylistInfo) -> None:
        """Upsert playlist info such as playlist name or
        playlist description. This method does not affect
        playlist track.

        Args:
            playlist_info (PlaylistInfo): PlaylistInfo object
        """
        pass

    @abstractmethod
    def get_playlist_track(self, playlist_id: str, spotify_id: str) -> PlaylistTrack:
        """Get the PlaylistTrack object with the spotify_id and plyalist_id.

        Args:
            playlist_id (str): playlist id
            spotify_id (str): track id

        Returns:
            PlaylistTrack: PlaylistTrack object if it exists else None
        """
