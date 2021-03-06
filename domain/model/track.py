from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Track:
    spotify_id: str
    song_name: str
    artist: str
    album_name: str
    bpm: float
    danceability: float
    energy: float
    image_url: str
    key: int
    mode: int
    preview_url: str


@dataclass(frozen=True)
class PlaylistTrack:
    id: str
    order: int
    track: Track
    created_at: datetime
    updated_at: datetime
