import os

from flask import Flask

from auth.oauth import init_oauth
from config import Config
from extensions import db, login_manager


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Ensure instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.google_login"

    init_oauth(app)

    from routes.admin_routes import admin_bp
    from routes.auth_routes import auth_bp
    from routes.user_routes import user_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(user_bp)

    with app.app_context():
        db.create_all()

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
