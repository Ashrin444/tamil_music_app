import os

from flask import Blueprint, abort, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from config import Config
from extensions import db
from models.song import Song

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.route("/", methods=["GET", "POST"])
@login_required
def dashboard():
    if current_user.role != "admin":
        abort(403)

    if request.method == "POST":
        title = request.form.get("title")
        audio = request.files.get("song")
        image = request.files.get("image")

        if not title or not audio:
            abort(400)

        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs("static/images", exist_ok=True)

        audio_name = secure_filename(audio.filename)
        audio.save(os.path.join(Config.UPLOAD_FOLDER, audio_name))

        image_name = "default.jpg"
        if image and image.filename:
            image_name = secure_filename(image.filename)
            image.save(os.path.join("static/images", image_name))

        song = Song(
            title=title,
            filename=audio_name,
            image=image_name
        )
        db.session.add(song)
        db.session.commit()

        return redirect(url_for("admin.dashboard"))

    songs = Song.query.all()
    return render_template("admin/dashboard.html", songs=songs)
