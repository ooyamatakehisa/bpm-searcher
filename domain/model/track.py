from dataclasses import dataclass


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
