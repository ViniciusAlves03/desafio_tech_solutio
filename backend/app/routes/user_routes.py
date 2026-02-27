from flask import Blueprint, request, jsonify, url_for
from app.utils.db import db
from app.models.user_model import User

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()

    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"error": "E-mail e senha são obrigatórios."}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Este e-mail já está cadastrado."}), 409

    new_user = User(email=data['email'])
    new_user.set_password(data['password'])

    db.session.add(new_user)
    db.session.commit()

    location_url = url_for('user_bp.get_user', id=new_user.id, _external=True)

    return jsonify(new_user.to_dict()), 201, {'Location': location_url}

@user_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200

@user_bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"error": "Usuário não encontrado."}), 404

    return jsonify(user.to_dict()), 200

@user_bp.route('/users/<int:id>', methods=['PATCH'])
def update_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"error": "Usuário não encontrado."}), 404

    data = request.get_json()

    if 'email' in data:
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user and existing_user.id != id:
            return jsonify({"error": "Este e-mail já está em uso por outra conta."}), 409
        user.email = data['email']

    if 'password' in data:
        user.set_password(data['password'])

    db.session.commit()
    return jsonify(user.to_dict()), 200

@user_bp.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"error": "Usuário não encontrado."}), 404

    db.session.delete(user)
    db.session.commit()

    return '', 204
