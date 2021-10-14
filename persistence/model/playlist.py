from . import db


class PlaylistInfoDataModel(db.Model):
    __tablename__ = "playlist"
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    desc = db.Column(db.Text, nullable=False)
    num_tracks = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(2048), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())

    playlist_track = db.relationship(
        "PlaylistTrackDataModel",
        backref="playlist",
    )
    user_playlist = db.relationship(
        "UserPlaylistDataModel",
        backref="playlist",
    )

    def __repr__(self):
        return f"<PlaylistInfoDataModel {self.name}>"
