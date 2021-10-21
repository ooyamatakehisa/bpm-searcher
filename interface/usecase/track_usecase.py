from abc import ABCMeta, abstractmethod
from typing import List

from domain.model.track import Track


class TrackUsecase(metaclass=ABCMeta):
    @abstractmethod
    def get_tracks_by_query(self, query: str) -> List[Track]:
        pass
