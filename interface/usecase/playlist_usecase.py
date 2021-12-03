from abc import ABCMeta, abstractmethod
from typing import List, Optional, Union

from domain.model.playlist import Playlist, PlaylistInfo
from domain.model.track import PlaylistTrack


class PlaylistUsecase(metaclass=ABCMeta):
    @abstractmethod
    def create_playlist(self, name: str, desc: str, uid: str) -> PlaylistInfo:
        """Create a new playlist for the user with the uid

        Args:
            name (str): playlist name
            desc (str): playlist description
            uid (str): user id
        """
        pass

    @abstractmethod
    def get_playlist_infos(self, uid: str) -> List[PlaylistInfo]:
        """Get all playlist infos of the user with the specifed uid

        Args:
            uid (str): user id

        Returns:
            List[PlaylistInfo]: list of PlyalistInfo objects
        """
        pass

    @abstractmethod
    def get_playlist(self, playlist_id: str, uid: str) -> Optional[Playlist]:
        """Get Playlist object with the playlist_id.

        Args:
            playlist_id (str): playlist id
            uid (str): user id

        Returns:
            Optional[Playlist]: Playlist object if it exists and the playlist is created
                by the user with the specified uid, else None.
        """
        pass

    @abstractmethod
    def delete_track(
        self,
        playlist_id: str,
        playlist_track_id: str,
        uid: str,
    ) -> Optional[Playlist]:
        """Delete track from specified playlist

        Args:
            playlist_id (str): playlist id
            playlist_track_id (str): playlist track id
            uid (str): user id

        Returns:
            Optional[Playlist]: Playlist object if it exists and the playlist is created
                by the user with the specified uid, else None.
        """
        pass

    @abstractmethod
    def update_playlist(
        self,
        kind: str,
        playlist_id: str,
        uid: str,
        name: str = None,
        desc: str = None,
        spotify_id: str = None,
    ) -> Optional[Union[Playlist, PlaylistInfo]]:
        """Update playlist info or tracks of the playlist with the specified playlist_id

        Args:
            kind (str): "track" or "info"
            playlist_id (str): playlist id
            uid (str): user id
            name (str, optional): playlist name. if "info" is set to "kind", this value
                must be specified. Defaults to None.
            desc (str, optional): playlist description. if "info" is set to "kind",
                this value must be specified. Defaults to None.
            spotify_id (str, optional): spotify id. if "track" is set to "kind",
                this value must be specified. Defaults to None.

        Returns:
            Optional[Union[Playlist, PlaylistInfo]]: Playlist or PlaylistInfo object
                if it exists and the playlist is created by the user with the specified
                uid, else None.
        """
        pass

    @abstractmethod
    def delete_playlist(self, playlist_id: str, uid: str) -> Optional[PlaylistInfo]:
        """Delete the playlist with the specified playlist_id

        Args:
            playlist_id (str): playlist id
            uid (str): user id

        Returns:
            Optional[PlaylistInfo]: Playlist object if it exists and the playlist is
                created by the user with the specified uid, else None.
        """
        pass

    @abstractmethod
    def patch_track_order(
        self,
        playlist_id: str,
        order_from: int,
        order_to: int,
        uid: str,
    ) -> Optional[List[PlaylistTrack]]:
        """Change the order of the tracks in the specified playlist.

        Args:
            playlist_id (str): playlist id
            order_from (int): the order from which oder is changed
            order_to (int): the order to which oder is changed
            uid (str): user id

        Returns:
            Optional[List[PlaylistTrack]]: List of PlyalistTrack objects if it exists,
                the playlist is created by the user with the specified uid
                and the spcified order is valid range.
        """
        pass
