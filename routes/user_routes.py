from flask import Blueprint, render_template
from flask_login import login_required

from models.song import Song

user_bp = Blueprint("user", __name__)

@user_bp.route("/")
@login_required
def home():
    songs = Song.query.all()

    # Convert SQLAlchemy objects → JSON-safe dicts
    songs_data = []
    for song in songs:
        songs_data.append({
            "id": song.id,
            "title": song.title,
            "filename": song.filename,
            "image": song.image
        })

    return render_template(
        "user/home.html",
        songs=songs_data
    )
