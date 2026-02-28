from flask import Blueprint, request, jsonify, url_for, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.di.di import container
from app.schemas.user_schema import user_schema, users_schema
from app.exceptions.api_exception_manager import APIExceptionManager

user_bp = Blueprint('user_bp', __name__)
user_service = container.get_user_service()

@user_bp.route('/users', methods=['POST'])
def create_user():
    try:
        data = user_schema.load(request.get_json())
        user = user_service.create_user(data)

        location_url = url_for('user_bp.get_user', id=user.id, _external=True)
        return jsonify(user_schema.dump(user)), 201, {'Location': location_url}

    except Exception as error:
        api_error = APIExceptionManager.build(error)
        return make_response(jsonify(api_error.toJSON()), api_error.code)


@user_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    try:
        users = user_service.get_all()
        return jsonify(users_schema.dump(users)), 200
    except Exception as error:
        api_error = APIExceptionManager.build(error)
        return make_response(jsonify(api_error.toJSON()), api_error.code)


@user_bp.route('/users/<int:id>', methods=['GET'])
@jwt_required()
def get_user(id):
    try:
        user = user_service.get_by_id(id)
        return jsonify(user_schema.dump(user)), 200
    except Exception as error:
        api_error = APIExceptionManager.build(error)
        return make_response(jsonify(api_error.toJSON()), api_error.code)


@user_bp.route('/users/<int:id>', methods=['PATCH'])
@jwt_required()
def update_user(id):
    try:
        data = user_schema.load(request.get_json(), partial=True)
        user = user_service.update_user(id, int(get_jwt_identity()), data)
        return jsonify(user_schema.dump(user)), 200
    except Exception as error:
        api_error = APIExceptionManager.build(error)
        return make_response(jsonify(api_error.toJSON()), api_error.code)


@user_bp.route('/users/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_user(id):
    try:
        user_service.delete_user(id, int(get_jwt_identity()))
        return '', 204
    except Exception as error:
        api_error = APIExceptionManager.build(error)
        return make_response(jsonify(api_error.toJSON()), api_error.code)
