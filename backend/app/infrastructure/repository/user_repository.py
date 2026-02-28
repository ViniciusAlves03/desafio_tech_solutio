from app.infrastructure.database.models.user_model import User
from app.utils.db import db
from app.application.port.user_repository_interface import IUserRepository
from app.application.domain.exception.domain_exceptions import ConflictError, RepositoryError

class UserRepository(IUserRepository):

    def create(self, user):
        try:
            db.session.add(user)
            db.session.commit()
            return user
        except Exception as error:
            db.session.rollback()
            raise RepositoryError("Erro ao salvar no banco de dados.", str(error))

    def get_by_id(self, user_id: int):
        try:
            return User.query.get(user_id)
        except Exception as error:
            raise RepositoryError("Erro ao buscar usuário por ID.", str(error))

    def get_by_email(self, email: str):
        try:
            return User.query.filter_by(email=email).first()
        except Exception as error:
            raise RepositoryError("Erro ao buscar usuário por e-mail.", str(error))

    def get_by_username(self, username: str):
        try:
            return User.query.filter_by(username=username).first()
        except Exception as error:
            raise RepositoryError("Erro ao buscar usuário por username.", str(error))

    def get_all(self):
        try:
            return User.query.all()
        except Exception as error:
            raise RepositoryError("Erro ao listar usuários.", str(error))

    def get_by_login_input(self, login_input: str):
        try:
            return User.query.filter(
                (User.email == login_input) | (User.username == login_input)
            ).first()
        except Exception as error:
            raise RepositoryError("Erro ao buscar usuário por credencial de login.", str(error))

    def update(self):
        try:
            db.session.commit()
        except Exception as error:
            db.session.rollback()
            raise RepositoryError("Erro ao atualizar no banco de dados.", str(error))

    def delete(self, user):
        try:
            db.session.delete(user)
            db.session.commit()
        except Exception as error:
            db.session.rollback()
            raise RepositoryError("Erro ao deletar no banco de dados.", str(error))
