from flask import Blueprint, request, jsonify, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.user_service import UserService
from app.repositories.user_repository import UserRepository

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or not all(k in data for k in ('username', 'email', 'password')):
        return jsonify({"error": "Usuário, e-mail e senha são obrigatórios."}), 400

    user, error = UserService.create_user(data)
    if error:
        return jsonify({"error": error}), 409

    location_url = url_for('user_bp.get_user', id=user.id, _external=True)
    return jsonify(user.to_dict()), 201, {'Location': location_url}

@user_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    users = UserRepository.get_all()
    return jsonify([user.to_dict() for user in users]), 200

@user_bp.route('/users/<int:id>', methods=['GET'])
@jwt_required()
def get_user(id):
    user = UserRepository.get_by_id(id)
    if not user:
        return jsonify({"error": "Usuário não encontrado."}), 404
    return jsonify(user.to_dict()), 200

@user_bp.route('/users/<int:id>', methods=['PATCH'])
@jwt_required()
def update_user(id):
    user, error = UserService.update_user(id, int(get_jwt_identity()), request.get_json())
    if error:
        return jsonify({"error": error}), 403 if "Acesso negado" in error else (409 if "em uso" in error else 404)
    return jsonify(user.to_dict()), 200

@user_bp.route('/users/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_user(id):
    success, error = UserService.delete_user(id, int(get_jwt_identity()))
    if error:
        return jsonify({"error": error}), 403 if "Acesso negado" in error else 404
    return '', 204
