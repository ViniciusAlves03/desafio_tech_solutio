from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from app.di.di import container
from app.exceptions.exceptions import ValidationException

auth_bp = Blueprint('auth_bp', __name__)

auth_service = container.get_auth_service()

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    login_input = data.get('login')
    password = data.get('password')

    if not login_input or not password:
        raise ValidationException("Login (e-mail ou usuário) e senha são obrigatórios")

    result = auth_service.login(login_input, password)
    return jsonify(result), 200

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    auth_service.logout(get_jwt()["jti"])
    return jsonify({"message": "Logout realizado com sucesso"}), 200
