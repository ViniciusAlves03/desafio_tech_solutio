from app.infrastructure.database.models import User
from app.application.port import IUserRepository
from app.application.domain.exception import NotFoundError, ForbiddenError, ConflictError
from app.utils import Messages

class UserService:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def get_all(self):
        try:
            return self.user_repository.get_all()
        except Exception as error:
            raise error

    def get_by_id(self, user_id):
        try:
            user = self.user_repository.get_by_id(user_id)
            if not user:
                raise NotFoundError(Messages.User.NOT_FOUND_TITLE, Messages.User.NOT_FOUND_DESC.format(user_id))
            return user
        except Exception as error:
            raise error

    def create_user(self, data):
        try:
            if self.user_repository.get_by_email(data['email']):
                raise ConflictError(Messages.User.EMAIL_CONFLICT)
            if self.user_repository.get_by_username(data['username']):
                raise ConflictError(Messages.User.USERNAME_CONFLICT)

            new_user = User(username=data['username'], email=data['email'])
            new_user.set_password(data['password'])

            return self.user_repository.create(new_user)
        except Exception as error:
            raise error

    def update_user(self, user_id, current_user_id, data):
        try:
            if current_user_id != user_id:
                raise ForbiddenError(Messages.User.FORBIDDEN_UPDATE)

            user = self.get_by_id(user_id)

            if 'username' in data:
                existing = self.user_repository.get_by_username(data['username'])
                if existing and existing.id != user_id:
                    raise ConflictError(Messages.User.USERNAME_CONFLICT)
                user.username = data['username']

            if 'email' in data:
                existing = self.user_repository.get_by_email(data['email'])
                if existing and existing.id != user_id:
                    raise ConflictError(Messages.User.EMAIL_CONFLICT)
                user.email = data['email']

            if 'password' in data:
                user.set_password(data['password'])

            self.user_repository.update(user)
            return user
        except Exception as error:
            raise error

    def delete_user(self, user_id, current_user_id):
        try:
            if current_user_id != user_id:
                raise ForbiddenError(Messages.User.FORBIDDEN_DELETE)

            user = self.get_by_id(user_id)
            self.user_repository.delete(user)
        except Exception as error:
            raise error
