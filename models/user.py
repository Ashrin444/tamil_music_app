from flask_login import UserMixin

from extensions import db, login_manager


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), unique=True, nullable=False)
    name = db.Column(db.String(200))
    role = db.Column(db.String(10))  # admin / user

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
