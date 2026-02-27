from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, current_user
from app.models.user_model import User
from app.utils.redis_client import redis_conn
from datetime import timedelta

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email', None)
    password = data.get('password', None)

    if not email or not password:
        return jsonify({"error": "E-mail e senha são obrigatórios"}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return jsonify({"error": "E-mail ou senha incorretos"}), 401

    access_token = create_access_token(identity=str(user.id), expires_delta=timedelta(hours=1))

    return jsonify(access_token=access_token, user=user.to_dict()), 200

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]

    redis_conn.set(jti, "", ex=timedelta(hours=1))

    return jsonify({"message": "Logout realizado com sucesso"}), 200
