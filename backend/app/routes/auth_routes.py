from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from app.models.user_model import User
from app.utils.redis_client import redis_conn
from datetime import timedelta

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    login_input = data.get('login', None)
    password = data.get('password', None)

    if not login_input or not password:
        return jsonify({"error": "Login (e-mail ou usuário) e senha são obrigatórios"}), 400

    user = User.query.filter(
        (User.email == login_input) | (User.username == login_input)
    ).first()

    if not user or not user.check_password(password):
        return jsonify({"error": "Credenciais incorretas"}), 401

    access_token = create_access_token(identity=str(user.id), expires_delta=timedelta(hours=1))

    return jsonify(access_token=access_token, user=user.to_dict()), 200

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    redis_conn.set(jti, "", ex=timedelta(hours=1))
    return jsonify({"message": "Logout realizado com sucesso"}), 200
