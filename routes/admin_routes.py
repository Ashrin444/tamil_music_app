import os

from flask import Blueprint, abort, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from config import Config
from extensions import db
from models.song import Song

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

# -------------------------------------------------
# Admin Dashboard – Upload & View Songs
# -------------------------------------------------
@admin_bp.route("/", methods=["GET", "POST"])
@login_required
def dashboard():
    """
    Admin dashboard:
    - Upload songs
    - View uploaded songs
    """
    # Enforce admin-only access (server-side)
    if current_user.role != "admin":
        abort(403, description="Admin access required")

    # Handle song upload
    if request.method == "POST":
        if "song" not in request.files:
            abort(400, description="No file uploaded")

        file = request.files["song"]
        title = request.form.get("title", "").strip()

        if not file.filename:
            abort(400, description="Empty filename")

        if not title:
            abort(400, description="Song title is required")

        # Ensure upload folder exists
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

        # Secure filename and save
        filename = secure_filename(file.filename)
        file_path = os.path.join(Config.UPLOAD_FOLDER, filename)
        file.save(file_path)

        # Save song metadata to DB
        song = Song(
            title=title,
            filename=filename
        )
        db.session.add(song)
        db.session.commit()

        return redirect(url_for("admin.dashboard"))

    # Fetch all uploaded songs
    songs = Song.query.order_by(Song.id.desc()).all()

    return render_template(
        "admin/dashboard.html",
        songs=songs
    )
