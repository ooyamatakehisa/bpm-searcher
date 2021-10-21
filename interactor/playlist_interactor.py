from datetime import datetime
from logging import Logger
from typing import List, Optional, Union
import uuid

from injector import inject, singleton

from domain.model.playlist import Playlist, PlaylistInfo
from domain.model.track import PlaylistTrack
from interface.repository.playlist_repository import PlaylistRepository
from interface.repository.track_repository import TrackRepository
from interface.usecase.track_usecase import TrackUsecase
from interface.usecase.playlist_usecase import PlaylistUsecase


@singleton
class PlaylistInteractor(PlaylistUsecase):
    @inject
    def __init__(
        self,
        logger: Logger,
        track_usecase: TrackUsecase,
        playlist_repository: PlaylistRepository,
        track_repository: TrackRepository,
    ) -> None:
        self.logger = logger
        self.track_usecase = track_usecase
        self.playlist_repository = playlist_repository
        self.track_repository = track_repository

    def create_playlist(self, name: str, desc: str, uid: str) -> PlaylistInfo:
        playlist_info = PlaylistInfo(
            id=uuid.uuid4(),
            uid=uid,
            name=name,
            desc=desc,
            image_url=None,
            num_tracks=0,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        self.playlist_repository.save_playlist_info(playlist_info)
        return playlist_info

    def get_playlist_infos(self, uid: str) -> List[PlaylistInfo]:
        return self.playlist_repository.get_playlist_infos(uid)

    def get_playlist(self, plyalist_id: str) -> Optional[Playlist]:
        return self.playlist_repository.get_playlist(plyalist_id)

    def delete_track(
        self,
        playlist_id: str,
        playlist_track_id: str
    ) -> Optional[Playlist]:
        playlist = self.playlist_repository.get_playlist(playlist_id)
        if playlist is None:
            self.logger.info("no playlist with the playlist_id")
            return None

        playlist_track = self.playlist_repository.get_playlist_track(playlist_track_id)
        if playlist_track is None:
            self.logger.info("no playlist_track with the playlist_track_id")
            return None

        playlist = self.playlist_repository.get_playlist(playlist_id)
        playlist = playlist.delete(playlist_track)
        self.playlist_repository.save_playlist(playlist)

        return playlist

    def update_playlist(
        self,
        kind: str,
        playlist_id: str,
        name: str = None,
        desc: str = None,
        spotify_id: str = None,
    ) -> Optional[Union[Playlist, PlaylistInfo]]:
        if kind == "info":
            playlist_info = self.playlist_repository.get_playlist_info(playlist_id)
            if playlist_info is None:
                self.logger.info("no playlist_info with the playlist id")
                return None

            playlist_info = PlaylistInfo(
                id=playlist_id,
                uid=playlist_info.uid,
                name=name,
                desc=desc,
                image_url=playlist_info.image_url,
                num_tracks=playlist_info.num_tracks,
                created_at=playlist_info.created_at,
                updated_at=datetime.utcnow(),
            )
            self.playlist_repository.save_playlist_info(playlist_info)

            return playlist_info

        elif kind == "track":
            playlist = self.playlist_repository.get_playlist(playlist_id)
            if playlist is None:
                self.logger.info("no playlist with the playlist id")
                return None

            track = self.track_repository.get_track_by_id(spotify_id)
            if track is None:
                self.logger.info("no track with the spotify id")
                return None

            playlist_track = PlaylistTrack(
                id=uuid.uuid4(),
                order=playlist.playlist_info.num_tracks + 1,
                track=track,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            playlist = playlist.add(playlist_track)
            self.playlist_repository.save_playlist(playlist)

            return playlist
