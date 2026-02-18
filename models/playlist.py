from extensions import db


class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

class PlaylistSong(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    playlist_id = db.Column(db.Integer)
    song_id = db.Column(db.Integer)
