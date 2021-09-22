from abc import ABCMeta, abstractmethod


class TrackUsecase(metaclass=ABCMeta):
    @abstractmethod
    def get_tracks(self, query: str) -> list:
        pass
