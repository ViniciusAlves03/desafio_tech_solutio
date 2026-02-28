from flask import Blueprint, request, jsonify, url_for, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from
from app.di.di import container
from app.infrastructure.database.schemas.user_schema import user_schema, users_schema
from app.ui.exception.api_exception_manager import APIExceptionManager

user_bp = Blueprint('user_bp', __name__)
user_service = container.get_user_service()

@user_bp.route('/users', methods=['POST'])
@swag_from('../docs/swagger/users/create.yml')
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
@swag_from('../docs/swagger/users/get_all.yml')
def get_users():
    try:
        users = user_service.get_all()
        return jsonify(users_schema.dump(users)), 200
    except Exception as error:
        api_error = APIExceptionManager.build(error)
        return make_response(jsonify(api_error.toJSON()), api_error.code)


@user_bp.route('/users/<int:id>', methods=['GET'])
@jwt_required()
@swag_from('../docs/swagger/users/get_by_id.yml')
def get_user(id):
    try:
        user = user_service.get_by_id(id)
        return jsonify(user_schema.dump(user)), 200
    except Exception as error:
        api_error = APIExceptionManager.build(error)
        return make_response(jsonify(api_error.toJSON()), api_error.code)


@user_bp.route('/users/<int:id>', methods=['PATCH'])
@jwt_required()
@swag_from('../docs/swagger/users/update.yml')
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
@swag_from('../docs/swagger/users/delete.yml')
def delete_user(id):
    try:
        user_service.delete_user(id, int(get_jwt_identity()))
        return '', 204
    except Exception as error:
        api_error = APIExceptionManager.build(error)
        return make_response(jsonify(api_error.toJSON()), api_error.code)
