from app.models.user_model import User
from app.repositories.user_repository import UserRepository

class UserService:
    @staticmethod
    def create_user(data):
        if UserRepository.get_by_email(data['email']):
            return None, "Este e-mail já está cadastrado."
        if UserRepository.get_by_username(data['username']):
            return None, "Este nome de usuário já está em uso."

        new_user = User(username=data['username'], email=data['email'])
        new_user.set_password(data['password'])
        return UserRepository.create(new_user), None

    @staticmethod
    def update_user(user_id, current_user_id, data):
        if current_user_id != user_id:
            return None, "Acesso negado. Você só pode alterar sua própria conta."

        user = UserRepository.get_by_id(user_id)
        if not user:
            return None, "Usuário não encontrado."

        if 'username' in data:
            existing = UserRepository.get_by_username(data['username'])
            if existing and existing.id != user_id:
                return None, "Este usuário já está em uso."
            user.username = data['username']

        if 'email' in data:
            existing = UserRepository.get_by_email(data['email'])
            if existing and existing.id != user_id:
                return None, "Este e-mail já está em uso."
            user.email = data['email']

        if 'password' in data:
            user.set_password(data['password'])

        UserRepository.update()
        return user, None

    @staticmethod
    def delete_user(user_id, current_user_id):
        if current_user_id != user_id:
            return False, "Acesso negado. Você só pode deletar sua própria conta."

        user = UserRepository.get_by_id(user_id)
        if not user:
            return False, "Usuário não encontrado."

        UserRepository.delete(user)
        return True, None
