from datetime import timedelta
from flask_jwt_extended import create_access_token
from app.repositories.user_repository import UserRepository
from app.utils.redis_client import redis_conn

class AuthService:
    @staticmethod
    def login(login_input, password):
        user = UserRepository.get_by_login_input(login_input)
        if not user or not user.check_password(password):
            return None, "Credenciais incorretas"

        access_token = create_access_token(identity=str(user.id), expires_delta=timedelta(hours=1))
        return {"access_token": access_token, "user": user.to_dict()}, None

    @staticmethod
    def logout(jti):
        redis_conn.set(jti, "", ex=timedelta(hours=1))
