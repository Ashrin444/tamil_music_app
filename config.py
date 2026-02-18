
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = "dev-secret-key"

    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///" + os.path.join(BASE_DIR, "instance", "database.db")
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

    ADMIN_EMAILS = {"ashrinlazer2005@gmail.com"}
    UPLOAD_FOLDER = "static/songs"
