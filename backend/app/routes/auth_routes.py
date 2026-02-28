from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from app.services.auth_service import AuthService

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    login_input = data.get('login')
    password = data.get('password')

    if not login_input or not password:
        return jsonify({"error": "Login (e-mail ou usuário) e senha são obrigatórios"}), 400

    result, error = AuthService.login(login_input, password)
    if error:
        return jsonify({"error": error}), 401

    return jsonify(result), 200

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    AuthService.logout(get_jwt()["jti"])
    return jsonify({"message": "Logout realizado com sucesso"}), 200
