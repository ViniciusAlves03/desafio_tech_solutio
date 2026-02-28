from flask import Blueprint, request, jsonify, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from app.exceptions.exceptions import ValidationException

user_bp = Blueprint('user_bp', __name__)

user_repo = UserRepository()
user_service = UserService(user_repository=user_repo)

@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or not all(k in data for k in ('username', 'email', 'password')):
        raise ValidationException("Usuário, e-mail e senha são obrigatórios.")

    user = user_service.create_user(data)
    location_url = url_for('user_bp.get_user', id=user.id, _external=True)
    return jsonify(user.to_dict()), 201, {'Location': location_url}

@user_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    users = user_service.get_all()
    return jsonify([user.to_dict() for user in users]), 200

@user_bp.route('/users/<int:id>', methods=['GET'])
@jwt_required()
def get_user(id):
    user = user_service.get_by_id(id)
    return jsonify(user.to_dict()), 200

@user_bp.route('/users/<int:id>', methods=['PATCH'])
@jwt_required()
def update_user(id):
    user = user_service.update_user(id, int(get_jwt_identity()), request.get_json())
    return jsonify(user.to_dict()), 200

@user_bp.route('/users/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_user(id):
    user_service.delete_user(id, int(get_jwt_identity()))
    return '', 204
