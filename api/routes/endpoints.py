from flask import Blueprint, jsonify, request
from api.repositories.user_repository import get_all_db_users
from sqlalchemy import text

from api.schemas.user_schema import UserLoginSchema, UserSchema
from api.services.note_service import fetch_notes_by_tag, fetch_notes_by_user, get_all_tags_from_users_notes
from api.services.user_service import add_user, sign_in_user, get_user
from db import db


routes_blueprint = Blueprint('routes', __name__)

@routes_blueprint.route('/', methods=['GET'])
def homePage():
    return jsonify('Returned from your Rest API!!!')


@routes_blueprint.route('/test_connection')
def test_connection():
    try:
        db.session.execute(text('SELECT 1'))
        db_uri = db.engine.url
        
        return f'Connection successful! Database URI: {db_uri}'
    except Exception as e:
        return f'Error: {str(e)}'
    

@routes_blueprint.route('/get_users', methods=['GET'])
def get_all_users():
    try:
        users_list = get_all_db_users()
        return jsonify(users_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@routes_blueprint.route('/users/register', methods=['POST'])
def register_user():
    try:
        user_data = UserSchema().load(request.json)

        user = add_user(user_data['username'], user_data['email'], user_data['password'])

        if 'error' in user:
            return jsonify(user), 400

        return jsonify(user), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@routes_blueprint.route('/users/login', methods=['POST'])
def login_user():
    try:

        login_data = UserLoginSchema().load(request.json)

        user = sign_in_user(login_data['username'], login_data['password'])

        if 'error' in user:
            return jsonify(user), 400

        return jsonify(user), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@routes_blueprint.route('/users/<int:user_id>/notes', methods=['GET'])
def get_notes_by_user(user_id):
    try:
        notes = fetch_notes_by_user(user_id)
        return jsonify(notes), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@routes_blueprint.route('/notes/tag/<string:tag_name>', methods=['GET'])
def get_notes_by_tag(tag_name):
    try:
        notes = fetch_notes_by_tag(tag_name)
        return jsonify(notes), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@routes_blueprint.route('/users/<int:user_id>/tags', methods=['GET'])
def get_all_tags(user_id):
    try:
        tags = get_all_tags_from_users_notes(user_id)
        return jsonify(tags), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@routes_blueprint.route('/users/<string:username>', methods=['GET'])
def get_user_by_username(username):
    try:
        user = get_user(username)
        return jsonify(user), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
