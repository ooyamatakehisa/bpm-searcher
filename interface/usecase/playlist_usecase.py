from abc import ABCMeta, abstractmethod
from typing import List

from domain.model.playlist import Playlist, PlaylistInfo


class PlaylistUsecase(metaclass=ABCMeta):
    @abstractmethod
    def create_playlist(self, name: str, desc: str, uid: str) -> None:
        """Create a new playlist for the user with the uid

        Args:
            name (str): playlist name
            desc (str): playlist description
            uid (str): user id
        """

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
    def get_playlist(self, playlist_id: str) -> Playlist:
        pass

    @abstractmethod
    def delete_track(self, playlist_id: str, playlist_track_id: str) -> bool:
        """Delete track from specified playlist

        Args:
            playlist_id (str): playlist id
            playlist_track_id (str): playlist track id

        Returns:
            bool: False if the playlist with the specified playlist id does not exits.
        """
        pass

    @abstractmethod
    def update_playlist(
        self,
        kind: str,
        playlist_id: str,
        name: str = None,
        desc: str = None,
        spotify_id: str = None,
    ) -> bool:
        """Update playlist info or tracks of the playlist with the specified playlist_id

        Args:
            kind (str): "track" or "info"
            playlist_id (str): playlist id
            name (str, optional): playlist name. if "info" is set to "kind", this value
                must be specified. Defaults to None.
            desc (str, optional): playlist description. if "info" is set to "kind",
                this value must be specified. Defaults to None.
            spotify_id (str, optional): spotify id. if "track" is set to "kind",
                this value must be specified. Defaults to None.

        Returns:
            bool: False if specified playlist does not exist
        """
        pass
