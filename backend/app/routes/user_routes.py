from flask import Blueprint, request, jsonify, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.db import db
from app.models.user_model import User

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()

    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Usuário, e-mail e senha são obrigatórios."}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Este e-mail já está cadastrado."}), 409

    if User.query.filter_by(username=data['username']).first():
        return jsonify({"error": "Este nome de usuário já está em uso."}), 409

    new_user = User(username=data['username'], email=data['email'])
    new_user.set_password(data['password'])

    db.session.add(new_user)
    db.session.commit()

    location_url = url_for('user_bp.get_user', id=new_user.id, _external=True)
    return jsonify(new_user.to_dict()), 201, {'Location': location_url}

@user_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200

@user_bp.route('/users/<int:id>', methods=['GET'])
@jwt_required()
def get_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"error": "Usuário não encontrado."}), 404
    return jsonify(user.to_dict()), 200

@user_bp.route('/users/<int:id>', methods=['PATCH'])
@jwt_required()
def update_user(id):
    current_user_id = int(get_jwt_identity())
    if current_user_id != id:
        return jsonify({"error": "Acesso negado. Você só pode alterar sua própria conta."}), 403
    user = User.query.get(id)
    if not user:
        return jsonify({"error": "Usuário não encontrado."}), 404

    data = request.get_json()

    if 'username' in data:
        existing_user = User.query.filter_by(username=data['username']).first()
        if existing_user and existing_user.id != id:
            return jsonify({"error": "Este usuário já está em uso."}), 409
        user.username = data['username']

    if 'email' in data:
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user and existing_user.id != id:
            return jsonify({"error": "Este e-mail já está em uso."}), 409
        user.email = data['email']

    if 'password' in data:
        user.set_password(data['password'])

    db.session.commit()
    return jsonify(user.to_dict()), 200

@user_bp.route('/users/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_user(id):
    current_user_id = int(get_jwt_identity())
    if current_user_id != id:
        return jsonify({"error": "Acesso negado. Você só pode deletar sua própria conta."}), 403
    user = User.query.get(id)
    if not user:
        return jsonify({"error": "Usuário não encontrado."}), 404

    db.session.delete(user)
    db.session.commit()
    return '', 204
