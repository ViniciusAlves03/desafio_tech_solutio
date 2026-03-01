from datetime import timedelta
from flask_jwt_extended import create_access_token

from app.application.port import IUserRepository
from app.infrastructure.redis import redis_conn
from app.application.domain.exception import AuthenticationError
from app.utils import Messages

class AuthService:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def login(self, login_input, password):
        try:
            user = self.user_repository.get_by_login_input(login_input)

            if not user or not user.check_password(password):
                raise AuthenticationError(Messages.Auth.INVALID_CREDENTIALS)

            access_token = create_access_token(identity=str(user.id), expires_delta=timedelta(hours=1))
            return {"access_token": access_token, "user": user.to_dict()}
        except Exception as error:
            raise error

    def logout(self, jti):
        try:
            redis_conn.set(jti, "", ex=timedelta(hours=1))
        except Exception as error:
            raise error
