from injector import inject, singleton
from typing import List

from domain.model.track import Track
from interface.repository.track_repository import TrackRepository
from interface.usecase.track_usecase import TrackUsecase


@singleton
class TrackInteractor(TrackUsecase):
    @inject
    def __init__(
        self,
        track_repository: TrackRepository,
    ) -> None:
        self.track_repository = track_repository

    def get_tracks_by_query(self, query: str) -> List[Track]:
        return self.get_tracks_by_query(query)
