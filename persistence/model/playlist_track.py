from . import db


class PlaylistTrackDataModel(db.Model):
    __tablename__ = "playlist_track"
    id = db.Column(db.String(50), primary_key=True)
    playlist_id = db.Column(
        db.String(50),
        db.ForeignKey('playlist.id'),
    )
    spotify_id = db.Column(db.String(190))
    order = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())

    def __repr__(self):
        return f"<PlaylistTrackDataModel {self.playlist_id},{self.spotify_id}>"
