from app.infrastructure.database.models import User
from app.application.port import IUserRepository
from app.infrastructure.database.postgres import ConnectionPostgres
from app.application.domain.exception import RepositoryError
from app.utils import Messages

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
                raise RepositoryError(Messages.Repository.ERR_SAVE_USER, str(error))

    def get_by_id(self, user_id: int) -> User:
        with self.db.get_session() as session:
            try:
                return session.query(User).filter(User.id == user_id).first()
            except Exception as error:
                raise RepositoryError(Messages.Repository.ERR_GET_USER_ID, str(error))

    def get_by_email(self, email: str) -> User:
        with self.db.get_session() as session:
            try:
                return session.query(User).filter(User.email == email).first()
            except Exception as error:
                raise RepositoryError(Messages.Repository.ERR_GET_USER_EMAIL, str(error))

    def get_by_username(self, username: str) -> User:
        with self.db.get_session() as session:
            try:
                return session.query(User).filter(User.username == username).first()
            except Exception as error:
                raise RepositoryError(Messages.Repository.ERR_GET_USER_USERNAME, str(error))

    def get_by_login_input(self, login_input: str) -> User:
        with self.db.get_session() as session:
            try:
                return session.query(User).filter(
                    (User.email == login_input) | (User.username == login_input)
                ).first()
            except Exception as error:
                raise RepositoryError(Messages.Repository.ERR_GET_USER_CRED, str(error))

    def get_all(self) -> list[User]:
        with self.db.get_session() as session:
            try:
                return session.query(User).all()
            except Exception as error:
                raise RepositoryError(Messages.Repository.ERR_GET_USERS, str(error))

    def update(self, user: User) -> None:
        with self.db.get_session() as session:
            try:
                session.merge(user)
                session.commit()
            except Exception as error:
                session.rollback()
                raise RepositoryError(Messages.Repository.ERR_UPDATE_USER, str(error))

    def delete(self, user: User) -> None:
        with self.db.get_session() as session:
            try:
                merged_user = session.merge(user)
                session.delete(merged_user)
                session.commit()
            except Exception as error:
                session.rollback()
                raise RepositoryError(Messages.Repository.ERR_DELETE_USER, str(error))
