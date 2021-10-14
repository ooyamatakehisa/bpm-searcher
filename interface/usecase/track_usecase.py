from abc import ABCMeta, abstractmethod


class TrackUsecase(metaclass=ABCMeta):
    @abstractmethod
    def get_tracks_by_query(self, query: str) -> list:
        pass

    @abstractmethod
    def get_tracks_by_ids(self, ids: list) -> list:
        pass
