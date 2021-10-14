from . import db


class UserPlaylistDataModel(db.Model):
    __tablename__ = "user_playlist"
    playlist_id = db.Column(
        db.String(50),
        db.ForeignKey('playlist.id'),
        primary_key=True,
    )
    uid = db.Column(db.String(190), primary_key=True)

    def __repr__(self):
        return f"<UserPlaylistDataModel {self.playlist_id},{self.uid}>"
