from abc import ABCMeta, abstractmethod
from typing import List

from domain.model.track import Track


class TrackRepository(metaclass=ABCMeta):
    @abstractmethod
    def get_track_by_id(self, track_id: str) -> Track:
        """Get Track objects with the spiecied track_id

        Args:
            track_id (str): track id

        Returns:
            Track: Track object with the specifed track_id
        """
        pass

    @abstractmethod
    def get_tracks_by_ids(self, track_ids: List[str]) -> List[Track]:
        """Get list of Track objects with the spiecied ids

        Args:
            ids (list): list of track ids

        Returns:
            List[Track]: list of Track objects with the specifed ids
        """
        pass

    @abstractmethod
    def get_tracks_by_query(self, query: str) -> List[Track]:
        """Get list of Track objects related to the spiecied query

        Args:
            query (str): search query

        Returns:
            List[Track]: list of Track objects related to the specifed query
        """
        pass
