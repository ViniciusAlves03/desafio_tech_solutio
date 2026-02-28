from app.models.user_model import User
from app.port.user_repository_interface import IUserRepository
from app.exceptions.exceptions import NotFoundException, ForbiddenException, ConflictException

class UserService:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def get_all(self):
        return self.user_repository.get_all()

    def get_by_id(self, user_id):
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise NotFoundException("Usuário não encontrado.")
        return user

    def create_user(self, data):
        if self.user_repository.get_by_email(data['email']):
            raise ConflictException("Este e-mail já está cadastrado.")
        if self.user_repository.get_by_username(data['username']):
            raise ConflictException("Este nome de usuário já está em uso.")

        new_user = User(username=data['username'], email=data['email'])
        new_user.set_password(data['password'])
        return self.user_repository.create(new_user)

    def update_user(self, user_id, current_user_id, data):
        if current_user_id != user_id:
            raise ForbiddenException("Acesso negado. Você só pode alterar sua própria conta.")

        user = self.get_by_id(user_id)

        if 'username' in data:
            existing = self.user_repository.get_by_username(data['username'])
            if existing and existing.id != user_id:
                raise ConflictException("Este usuário já está em uso.")
            user.username = data['username']

        if 'email' in data:
            existing = self.user_repository.get_by_email(data['email'])
            if existing and existing.id != user_id:
                raise ConflictException("Este e-mail já está em uso.")
            user.email = data['email']

        if 'password' in data:
            user.set_password(data['password'])

        self.user_repository.update()
        return user

    def delete_user(self, user_id, current_user_id):
        if current_user_id != user_id:
            raise ForbiddenException("Acesso negado. Você só pode deletar sua própria conta.")

        user = self.get_by_id(user_id)
        self.user_repository.delete(user)
