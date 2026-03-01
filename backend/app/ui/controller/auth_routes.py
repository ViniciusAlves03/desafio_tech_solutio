from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt
from flasgger import swag_from
from app.di.di import container
from app.ui.exception.api_exception_manager import APIExceptionManager
from app.application.domain.exception.exceptions import ValidationError
from app.utils.messages import Messages

auth_bp = Blueprint('auth_bp', __name__)
auth_service = container.get_auth_service()

@auth_bp.route('/login', methods=['POST'])
@swag_from('../docs/swagger/auth/login.yml')
def login():
    try:
        data = request.get_json()
        login_input = data.get('login')
        password = data.get('password')

        if not login_input or not password:
            raise ValidationError(Messages.Validation.MISSING_LOGIN_CREDS)

        result = auth_service.login(login_input, password)
        return jsonify(result), 200
    except Exception as error:
        api_error = APIExceptionManager.build(error)
        return make_response(jsonify(api_error.toJSON()), api_error.code)

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
@swag_from('../docs/swagger/auth/logout.yml')
def logout():
    try:
        auth_service.logout(get_jwt()["jti"])
        return jsonify({"message": "Logged out successfully."}), 200
    except Exception as error:
        api_error = APIExceptionManager.build(error)
        return make_response(jsonify(api_error.toJSON()), api_error.code)
