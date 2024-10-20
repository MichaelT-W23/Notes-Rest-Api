from api.models.db_models import User
from db import db

def create_user(username: str, email: str, password_hash: str) -> User:
    new_user = User(username=username, email=email, password_hash=password_hash)
    db.session.add(new_user)
    db.session.commit()
    return new_user

def get_user_by_username(username: str) -> User:
    return User.query.filter_by(username=username).first()

def get_all_db_users():
    try:
        users = User.query.all()
        return [user.to_dict() for user in users]
    except Exception as e:
        db.session.rollback()
        raise e