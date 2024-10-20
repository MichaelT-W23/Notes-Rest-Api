from api.errors.custom_exceptions import InvalidCredentialsError
from api.repositories.user_repository import create_user, get_user_by_username
from werkzeug.security import check_password_hash, generate_password_hash


def add_user(username: str, email: str, password: str) -> dict:

    password_hash = generate_password_hash(password)
    
    if get_user_by_username(username):
        return {"error": "Username already exists"}
    
    user = create_user(username, email, password_hash)
    
    return user.to_dict()


def sign_in_user(username: str, password: str) -> dict:
    user = get_user_by_username(username)

    if user and check_password_hash(user.password_hash, password):
        return {"message": "User signed in successfully", "user": user.to_dict()}
    else:
        raise InvalidCredentialsError()
    
def get_user(username: str) -> dict:
    try: 
        user = get_user_by_username(username)
        return user.to_dict()
    except Exception:
        raise InvalidCredentialsError()
