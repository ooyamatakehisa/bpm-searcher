from logging import Logger
from typing import List, Optional

from injector import inject, singleton
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

from domain.model.playlist import Playlist, PlaylistInfo
from domain.model.track import PlaylistTrack
from interface.repository.playlist_repository import PlaylistRepository
from interface.repository.track_repository import TrackRepository
from persistence.model.playlist import PlaylistInfoDataModel
from persistence.model.user_playlist import UserPlaylistDataModel
from persistence.model.playlist_track import PlaylistTrackDataModel


@singleton
class PlaylistRepositoryImpl(PlaylistRepository):
    @inject
    def __init__(
        self,
        db: SQLAlchemy,
        logger: Logger,
        track_repository: TrackRepository
    ):
        self.db = db
        self.logger = logger
        self.track_repository = track_repository

    def get_playlist_infos(self, uid: str) -> List[PlaylistInfo]:
        user_playlist_datas = self.db.session.query(UserPlaylistDataModel) \
            .filter_by(uid=uid)

        playlist_ids = [
            user_playlist_data.playlist_id
            for user_playlist_data in user_playlist_datas
        ]

        if len(playlist_ids) == 0:
            return []

        in_exp = PlaylistInfoDataModel.id.in_(playlist_ids)
        playlist_info_datas = self.db.session.query(PlaylistInfoDataModel) \
            .filter(in_exp)

        playlist_infos = [
            PlaylistInfo(
                id=playlist_info_data.id,
                uid=uid,
                name=playlist_info_data.name,
                desc=playlist_info_data.desc,
                image_url=playlist_info_data.image_url,
                num_tracks=playlist_info_data.num_tracks,
                created_at=playlist_info_data.created_at,
                updated_at=playlist_info_data.updated_at,
            )
            for playlist_info_data in playlist_info_datas
        ]
        return playlist_infos

    def get_playlist(self, playlist_id: str) -> Optional[Playlist]:
        playlist_info = self.get_playlist_info(playlist_id)
        if playlist_info is None:
            return None

        playlist_tracks = self.get_playlist_tracks(playlist_id)
        return Playlist(playlist_info=playlist_info, playlist_tracks=playlist_tracks)

    def get_playlist_info(self, playlist_id: str) -> Optional[PlaylistInfo]:
        try:
            playlist_info_data = self.db.session.query(PlaylistInfoDataModel) \
                .filter_by(id=playlist_id) \
                .first()

            user_playlist = self.db.session.query(UserPlaylistDataModel) \
                .filter_by(playlist_id=playlist_id) \
                .first()

            if playlist_info_data is not None:
                return PlaylistInfo(
                    id=playlist_info_data.id,
                    uid=user_playlist.uid,
                    name=playlist_info_data.name,
                    desc=playlist_info_data.desc,
                    image_url=playlist_info_data.image_url,
                    num_tracks=playlist_info_data.num_tracks,
                    created_at=playlist_info_data.created_at,
                    updated_at=playlist_info_data.updated_at,
                )

        except SQLAlchemyError as e:
            self.db.session.rollback()
            self.logger.error(f"failed to get playlist info: {e}")
            raise e

        finally:
            self.db.session.close()

    def get_playlist_track(self, playlist_track_id: str) -> Optional[PlaylistTrack]:
        try:
            playlist_track_data = self.db.session.query(PlaylistTrackDataModel) \
                .filter_by(id=playlist_track_id) \
                .first()

            spotify_id = playlist_track_data.spotify_id
            track = self.track_repository.get_track_by_id(spotify_id)

            if playlist_track_data is not None:
                return PlaylistTrack(
                    id=playlist_track_data.id,
                    order=playlist_track_data.order,
                    track=track,
                    created_at=playlist_track_data.created_at,
                    updated_at=playlist_track_data.updated_at,
                )

        except SQLAlchemyError as e:
            self.db.session.rollback()
            self.logger.error(f"failed to get a PlaylistTrack object: {e}")
            raise e

        finally:
            self.db.session.close()
        pass

    def get_playlist_tracks(self, playlist_id: str) -> List[PlaylistTrack]:
        try:
            playlist_track_datas = self.db.session.query(PlaylistTrackDataModel) \
                .filter_by(playlist_id=playlist_id) \
                .order_by(PlaylistTrackDataModel.order)

            track_ids = [
                playlist_track_data.spotify_id
                for playlist_track_data in playlist_track_datas
            ]

            if len(track_ids) == 0:
                return []

            tracks = self.track_repository.get_tracks_by_ids(track_ids)

            return [
                PlaylistTrack(
                    id=playlist_track_data.id,
                    track=tracks[idx],
                    order=playlist_track_data.order,
                    created_at=playlist_track_data.created_at,
                    updated_at=playlist_track_data.updated_at,
                )
                for idx, playlist_track_data in enumerate(playlist_track_datas)
            ]

        except SQLAlchemyError as e:
            self.db.session.rollback()
            self.logger.error(f"failed to get playlist tracks: {e}")
            raise e

        finally:
            self.db.session.close()

    def save_playlist(self, playlist: Playlist) -> None:
        playlist_info = playlist.playlist_info
        old_playlist_tracks = self.get_playlist_tracks(playlist_info.id)
        try:
            playlist_info_data = PlaylistInfoDataModel(
                id=playlist_info.id,
                name=playlist_info.name,
                desc=playlist_info.desc,
                image_url=playlist_info.image_url,
                num_tracks=playlist_info.num_tracks,
                created_at=playlist_info.created_at,
                updated_at=playlist_info.updated_at,
            )
            self.db.session.merge(playlist_info_data)

            user_playlist_info_data = UserPlaylistDataModel(
                playlist_id=playlist_info.id,
                uid=playlist_info.uid,
            )
            self.db.session.merge(user_playlist_info_data)

            # upsert playlist_track
            for playlist_track in playlist.playlist_tracks:
                playlist_track_data = PlaylistTrackDataModel(
                    id=playlist_track.id,
                    playlist_id=playlist_info.id,
                    spotify_id=playlist_track.track.spotify_id,
                    order=playlist_track.order,
                    created_at=playlist_track.created_at,
                    updated_at=playlist_track.updated_at,
                )
                self.db.session.merge(playlist_track_data)

            # delete playlist_track
            old_ids = set(map(lambda x: x.id, old_playlist_tracks))
            new_ids = set(map(lambda x: x.id, playlist.playlist_tracks))
            delete_playlist_track_ids = old_ids - new_ids

            if len(delete_playlist_track_ids) > 0:
                in_exp = PlaylistTrackDataModel.id.in_(delete_playlist_track_ids)
                playlist_track_data = self.db.session.query(PlaylistTrackDataModel) \
                    .filter(in_exp) \
                    .delete()

            self.db.session.commit()

        except SQLAlchemyError as e:
            self.db.session.rollback()
            self.logger.error(f"failed to save playlist: {e}")
            raise e

        finally:
            self.db.session.close()

    def save_playlist_info(self, playlist_info: PlaylistInfo) -> None:
        try:
            playlist_info_data = PlaylistInfoDataModel(
                id=playlist_info.id,
                name=playlist_info.name,
                desc=playlist_info.desc,
                image_url=playlist_info.image_url,
                num_tracks=playlist_info.num_tracks,
                created_at=playlist_info.created_at,
                updated_at=playlist_info.updated_at,
            )
            self.db.session.merge(playlist_info_data)

            user_playlist_info_data = UserPlaylistDataModel(
                playlist_id=playlist_info.id,
                uid=playlist_info.uid,
            )
            self.db.session.merge(user_playlist_info_data)

            self.db.session.commit()

        except SQLAlchemyError as e:
            self.db.session.rollback()
            self.logger.error(f"failed to save playlist info: {e}")
            raise e

        finally:
            self.db.session.close()
