from flask import Blueprint, abort, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from extensions import db
from models.playlist import Playlist, PlaylistSong
from models.song import Song

user_bp = Blueprint("user", __name__)

# -------------------------------------------------
# User Home (All Songs + Playlists)
# -------------------------------------------------
@user_bp.route("/")
@login_required
def home():
    """
    User landing page:
    - List all songs
    - List user's playlists
    """
    songs = Song.query.all()
    playlists = Playlist.query.filter_by(user_id=current_user.id).all()

    return render_template(
        "user/home.html",
        songs=songs,
        playlists=playlists
    )

# -------------------------------------------------
# Create Playlist
# -------------------------------------------------
@user_bp.route("/playlist/create", methods=["POST"])
@login_required
def create_playlist():
    """
    Create a new playlist for the logged-in user
    """
    name = request.form.get("name")

    if not name:
        abort(400, description="Playlist name is required")

    playlist = Playlist(
        name=name.strip(),
        user_id=current_user.id
    )

    db.session.add(playlist)
    db.session.commit()

    return redirect(url_for("user.home"))

# -------------------------------------------------
# Add Song to Playlist
# -------------------------------------------------
@user_bp.route("/playlist/add", methods=["POST"])
@login_required
def add_song_to_playlist():
    """
    Add a song to a user's playlist
    """
    playlist_id = request.form.get("playlist_id")
    song_id = request.form.get("song_id")

    if not playlist_id or not song_id:
        abort(400, description="Invalid playlist or song")

    playlist = Playlist.query.get_or_404(playlist_id)

    # Ownership check (critical security rule)
    if playlist.user_id != current_user.id:
        abort(403, description="Unauthorized playlist access")

    # Prevent duplicate entries
    exists = PlaylistSong.query.filter_by(
        playlist_id=playlist_id,
        song_id=song_id
    ).first()

    if not exists:
        db.session.add(
            PlaylistSong(
                playlist_id=playlist_id,
                song_id=song_id
            )
        )
        db.session.commit()

    return redirect(url_for("user.home"))

# -------------------------------------------------
# View Playlist
# -------------------------------------------------
@user_bp.route("/playlist/<int:playlist_id>")
@login_required
def view_playlist(playlist_id):
    """
    View songs inside a playlist
    """
    playlist = Playlist.query.get_or_404(playlist_id)

    # Ownership enforcement
    if playlist.user_id != current_user.id:
        abort(403, description="Unauthorized access")

    song_links = PlaylistSong.query.filter_by(
        playlist_id=playlist_id
    ).all()

    song_ids = [link.song_id for link in song_links]
    songs = Song.query.filter(Song.id.in_(song_ids)).all()

    return render_template(
        "user/playlist.html",
        playlist=playlist,
        songs=songs
    )

# -------------------------------------------------
# Remove Song from Playlist
# -------------------------------------------------
@user_bp.route("/playlist/remove", methods=["POST"])
@login_required
def remove_song_from_playlist():
    """
    Remove a song from a playlist
    """
    playlist_id = request.form.get("playlist_id")
    song_id = request.form.get("song_id")

    playlist = Playlist.query.get_or_404(playlist_id)

    if playlist.user_id != current_user.id:
        abort(403)

    entry = PlaylistSong.query.filter_by(
        playlist_id=playlist_id,
        song_id=song_id
    ).first_or_404()

    db.session.delete(entry)
    db.session.commit()

    return redirect(url_for("user.view_playlist", playlist_id=playlist_id))
