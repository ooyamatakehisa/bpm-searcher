from abc import ABCMeta, abstractmethod
from typing import List, Optional

from domain.model.playlist import Playlist, PlaylistInfo
from domain.model.track import PlaylistTrack


class PlaylistRepository(metaclass=ABCMeta):
    @abstractmethod
    def get_playlist_infos(self, uid: str) -> List[PlaylistInfo]:
        """Get list of PlaylistInfo objects of the user with the uid.
        If no playlist exists, return the list with no element.

        Args:
            uid (str): user id

        Returns:
            List[PlaylistInfo]: list of PlaylistInfo objects
        """
        pass

    @abstractmethod
    def get_playlist(playlist_id: str) -> Optional[Playlist]:
        """Get Playlist object with the playlist_id.

        Args:
            playlist_id (str): playlist id

        Returns:
            Optional[Playlist]: Playlist object if it exists, else None.
        """
        pass

    @abstractmethod
    def get_playlist_info(playlist_id: str) -> Optional[PlaylistInfo]:
        """Get PlaylistInfo object of the playlist with specified playlist_id.
        PlaylistInfo include metadata of playlist such as name or descrption.

        Args:
            playlist_id (str): playlist id

        Returns:
            PlaylistInfo: PlaylistInfo object if it exists, else None.
        """
        pass

    @abstractmethod
    def get_playlist_track(self, playlist_track_id: str) -> Optional[PlaylistTrack]:
        """Get the PlaylistTrack object with the playlist_track_id.

        Args:
            playlist_track_id (str): playlist track id

        Returns:
            PlaylistTrack: PlaylistTrack object if it exists else None
        """

    @abstractmethod
    def get_playlist_tracks(playlist_id: str) -> List[PlaylistTrack]:
        """Get list of PlaylistTrack objects of the playlist with the specified playlist
        If no playlist_track exists, return the list with no element.

        Args:
            playlist_id (str): playlist id

        Returns:
            List[PlaylistTrack]: list of PlaylistTrack objects.
        """
        pass

    @abstractmethod
    def save_playlist(self, playlist: Playlist) -> None:
        """Upsert Playlist object.

        Args:
            playlist (Playlist): Playlist object
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
    def delete_playlist(self, playlist_id: str) -> None:
        """Delete the playlist with the specified playlist_id

        Args:
            playlist_id (str): playlist id
        """
        pass
