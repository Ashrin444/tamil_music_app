from flask import Blueprint, abort, redirect, session, url_for
from flask_login import login_required, login_user, logout_user

from auth.oauth import oauth
from config import Config
from extensions import db
from models.user import User

auth_bp = Blueprint("auth", __name__)

# -------------------------------------------------
# Google OAuth Login
# -------------------------------------------------
@auth_bp.route("/login/google")
def google_login():
    """
    Redirect user to Google OAuth consent screen
    """
    return oauth.google.authorize_redirect(
        url_for("auth.google_callback", _external=True)
    )

# -------------------------------------------------
# Google OAuth Callback
# -------------------------------------------------
@auth_bp.route("/login/google/callback")
def google_callback():
    """
    Handle Google OAuth response securely
    """
    try:
        # Exchange authorization code for token
        token = oauth.google.authorize_access_token()
    except Exception:
        abort(401, description="Google authentication failed")

    # Fetch user profile from Google
    resp = oauth.google.get("userinfo")
    if resp.status_code != 200:
        abort(401, description="Unable to fetch user information")

    user_info = resp.json()

    email = user_info.get("email")
    name = user_info.get("name", "User")

    if not email:
        abort(400, description="Google account email not available")

    # Lookup user in database
    user = User.query.filter_by(email=email).first()

    if not user:
        # Assign role using server-side whitelist
        role = "admin" if email in Config.ADMIN_EMAILS else "user"

        user = User(
            email=email,
            name=name,
            role=role
        )
        db.session.add(user)
        db.session.commit()

    # Login user via Flask-Login
    login_user(user)

    # Redirect user based on role
    return redirect(
        url_for("admin.dashboard") if user.role == "admin"
        else url_for("user.home")
    )

# -------------------------------------------------
# Logout
# -------------------------------------------------
@auth_bp.route("/logout")
@login_required
def logout():
    """
    Logout user and clear session safely
    """
    logout_user()
    session.clear()
    return redirect(url_for("auth.google_login"))
