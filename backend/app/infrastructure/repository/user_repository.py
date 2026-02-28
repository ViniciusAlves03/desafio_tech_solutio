from sqlalchemy.exc import IntegrityError
from app.infrastructure.database.models.user_model import User
from app.application.port.user_repository_interface import IUserRepository
from app.infrastructure.database.postgres.connection_postgres import ConnectionPostgres
from app.application.domain.exception.domain_exceptions import ConflictError, RepositoryError

class UserRepository(IUserRepository):
    def __init__(self, db_connection: ConnectionPostgres):
        self.db = db_connection

    def create(self, user: User) -> User:
        with self.db.get_session() as session:
            try:
                session.add(user)
                session.commit()
                session.refresh(user)
                return user
            except Exception as error:
                session.rollback()
                raise RepositoryError("Erro ao salvar o usuário no banco de dados.", str(error))

    def get_by_id(self, user_id: int) -> User:
        with self.db.get_session() as session:
            try:
                return session.query(User).filter(User.id == user_id).first()
            except Exception as error:
                raise RepositoryError("Erro ao buscar usuário por ID.", str(error))

    def get_by_email(self, email: str) -> User:
        with self.db.get_session() as session:
            try:
                return session.query(User).filter(User.email == email).first()
            except Exception as error:
                raise RepositoryError("Erro ao buscar usuário por e-mail.", str(error))

    def get_by_username(self, username: str) -> User:
        with self.db.get_session() as session:
            try:
                return session.query(User).filter(User.username == username).first()
            except Exception as error:
                raise RepositoryError("Erro ao buscar usuário por username.", str(error))

    def get_by_login_input(self, login_input: str) -> User:
        with self.db.get_session() as session:
            try:
                return session.query(User).filter(
                    (User.email == login_input) | (User.username == login_input)
                ).first()
            except Exception as error:
                raise RepositoryError("Erro ao buscar usuário por credencial de login.", str(error))

    def get_all(self) -> list[User]:
        with self.db.get_session() as session:
            try:
                return session.query(User).all()
            except Exception as error:
                raise RepositoryError("Erro ao listar usuários.", str(error))

    def update(self, user: User) -> None:
        with self.db.get_session() as session:
            try:
                session.merge(user)
                session.commit()
            except Exception as error:
                session.rollback()
                raise RepositoryError("Erro ao atualizar o usuário no banco de dados.", str(error))

    def delete(self, user: User) -> None:
        with self.db.get_session() as session:
            try:
                merged_user = session.merge(user)
                session.delete(merged_user)
                session.commit()
            except Exception as error:
                session.rollback()
                raise RepositoryError("Erro ao deletar o usuário no banco de dados.", str(error))
