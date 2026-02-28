from datetime import timedelta
from flask_jwt_extended import create_access_token
from app.port.user_repository_interface import IUserRepository
from app.port.auth_service_interface import IAuthService
from app.utils.redis_client import redis_conn
from app.exceptions.exceptions import UnauthorizedException

class AuthService(IAuthService):
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def login(self, login_input, password):
        user = self.user_repository.get_by_login_input(login_input)

        if not user or not user.check_password(password):
            raise UnauthorizedException("Credenciais incorretas")

        access_token = create_access_token(identity=str(user.id), expires_delta=timedelta(hours=1))
        return {"access_token": access_token, "user": user.to_dict()}

    def logout(self, jti):
        redis_conn.set(jti, "", ex=timedelta(hours=1))
