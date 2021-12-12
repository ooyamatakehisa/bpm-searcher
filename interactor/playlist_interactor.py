from datetime import datetime
from logging import Logger
from typing import List, Optional
import uuid

from injector import inject, singleton

from domain.model.playlist import Playlist, PlaylistInfo
from domain.model.track import PlaylistTrack
from interface.repository.playlist_repository import PlaylistRepository
from interface.repository.track_repository import TrackRepository
from interface.usecase.playlist_usecase import PlaylistUsecase


@singleton
class PlaylistInteractor(PlaylistUsecase):
    @inject
    def __init__(
        self,
        logger: Logger,
        playlist_repository: PlaylistRepository,
        track_repository: TrackRepository,
    ) -> None:
        self.logger = logger
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

    def get_playlist(self, plyalist_id: str, uid: str) -> Optional[Playlist]:
        playlist = self.playlist_repository.get_playlist(plyalist_id)
        if playlist is None:
            self.logger.info("no playlist with the playlist_id")
            return None

        if playlist.playlist_info.uid != uid:
            self.logger.info("specified playlist is not created by the user")
            return None

        return playlist

    def delete_playlist(self, playlist_id: str, uid: str) -> Optional[PlaylistInfo]:
        playlist_info = self.playlist_repository.get_playlist_info(playlist_id)
        if playlist_info is None:
            self.logger.info("no playlist with the playlist_id")
            return None

        if playlist_info.uid != uid:
            self.logger.info("specified playlist is not created by the user")
            return None

        self.playlist_repository.delete_playlist(playlist_id)
        return playlist_info

    def delete_track(
        self, playlist_id: str, playlist_track_id: str, uid: str
    ) -> Optional[Playlist]:
        playlist = self.playlist_repository.get_playlist(playlist_id)
        if playlist is None:
            self.logger.info("no playlist with the playlist_id")
            return None

        if playlist.playlist_info.uid != uid:
            self.logger.info("specified playlist is not created by the user")
            return None

        playlist_track = self.playlist_repository.get_playlist_track(playlist_track_id)
        if playlist_track is None:
            self.logger.info("no playlist_track with the playlist_track_id")
            return None

        playlist = playlist.delete(playlist_track)
        self.playlist_repository.save_playlist(playlist)

        return playlist

    def patch_playlist_info(
        self,
        playlist_id: str,
        uid: str,
        name: str,
        desc: str,
    ) -> Optional[PlaylistInfo]:
        playlist_info = self.playlist_repository.get_playlist_info(playlist_id)
        if playlist_info is None:
            self.logger.info("no playlist_info with the playlist id")
            return None

        if playlist_info.uid != uid:
            self.logger.info("specified playlist is not created by the user")
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

    def update_playlist(
        self,
        playlist_id: str,
        uid: str,
        spotify_id: str,
    ) -> Optional[Playlist]:
        playlist = self.playlist_repository.get_playlist(playlist_id)
        if playlist is None:
            self.logger.info("no playlist with the playlist id")
            return None

        if playlist.playlist_info.uid != uid:
            self.logger.info("specified playlist is not created by the user")
            return None

        track = self.track_repository.get_track_by_id(spotify_id)
        if track is None:
            self.logger.info("no track with the spotify id")
            return None

        playlist = playlist.add(track)
        self.playlist_repository.save_playlist(playlist)

        return playlist

    def patch_track_order(
        self, playlist_id: str, order_from: int, order_to: int, uid: str
    ) -> Optional[List[PlaylistTrack]]:
        playlist = self.playlist_repository.get_playlist(playlist_id)
        if playlist is None:
            self.logger.info("no playlist with the playlist id")
            return None

        if playlist.playlist_info.uid != uid:
            self.logger.info("specified playlist is not created by the user")
            return None

        playlist = playlist.patch_track_order(order_from, order_to)
        if playlist is None:
            self.logger.info("specified order is invalid")
            return None

        self.playlist_repository.save_playlist(playlist)
        return playlist.playlist_tracks
