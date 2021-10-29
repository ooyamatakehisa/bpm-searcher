from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import List
import uuid

from domain.model.track import PlaylistTrack, Track


@dataclass(frozen=True)
class PlaylistInfo:
    id: str
    uid: str
    name: str
    desc: str
    num_tracks: int
    image_url: str
    created_at: datetime
    updated_at: datetime

    # TODO: add constraints to name or desc
    # num_tracks must be less than 50 because spotify api "get tracks from ids"
    # only receive ids


@dataclass(frozen=True)
class Playlist:
    playlist_info: PlaylistInfo
    playlist_tracks: List[PlaylistTrack]

    def delete(self, playlist_track: PlaylistTrack) -> Playlist:
        """Remove the specified playlist_track from this playlist.
        Playlist has own image_url and this is the same as that of the first track in
        this playlist.

        Args:
            playlist_track (PlaylistTrack): playlist_track to remove

        Returns:
            Playlist: new playlist from which the specified playlist_track is removed
        """
        playlist_tracks = []
        for playlist_track_ in self.playlist_tracks:
            if playlist_track_.order < playlist_track.order:
                playlist_tracks.append(playlist_track_)

            elif playlist_track_.order > playlist_track.order:
                new_playlist_track = PlaylistTrack(
                    id=playlist_track_.id,
                    order=playlist_track_.order - 1,
                    track=playlist_track_.track,
                    created_at=playlist_track_.created_at,
                    updated_at=datetime.utcnow(),
                )
                playlist_tracks.append(new_playlist_track)

        if len(playlist_tracks) == 0:
            image_url = None
        else:
            image_url = playlist_tracks[0].track.image_url

        playlist_info = PlaylistInfo(
            id=self.playlist_info.id,
            uid=self.playlist_info.uid,
            name=self.playlist_info.name,
            desc=self.playlist_info.desc,
            image_url=image_url,
            num_tracks=self.playlist_info.num_tracks - 1,
            created_at=self.playlist_info.created_at,
            updated_at=datetime.utcnow(),
        )

        return Playlist(playlist_info=playlist_info, playlist_tracks=playlist_tracks)

    def add(self, track: Track) -> Playlist:
        """Add the specifed track to this playlist

        Args:
            track (Track): Track to add

        Returns:
            Playlist: new playlist to which new track is added
        """
        playlist_track = PlaylistTrack(
            id=uuid.uuid4(),
            order=self.playlist_info.num_tracks + 1,
            track=track,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        playlist_tracks = self.playlist_tracks + [playlist_track]

        playlist_info = PlaylistInfo(
            id=self.playlist_info.id,
            uid=self.playlist_info.uid,
            name=self.playlist_info.name,
            desc=self.playlist_info.desc,
            image_url=playlist_tracks[0].track.image_url,
            num_tracks=self.playlist_info.num_tracks + 1,
            created_at=self.playlist_info.created_at,
            updated_at=playlist_track.updated_at,
        )
        return Playlist(playlist_info=playlist_info, playlist_tracks=playlist_tracks)
