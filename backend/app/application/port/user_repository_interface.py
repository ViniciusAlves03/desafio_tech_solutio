from abc import ABC, abstractmethod
from app.infrastructure.database.models.user_model import User

class IUserRepository(ABC):
    @abstractmethod
    def create(self, user: User) -> User:
        pass

    @abstractmethod
    def get_by_id(self, user_id: int) -> User:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> User:
        pass

    @abstractmethod
    def get_by_username(self, username: str) -> User:
        pass

    @abstractmethod
    def get_all(self) -> list[User]:
        pass

    @abstractmethod
    def get_by_login_input(self, login_input: str) -> User:
        pass

    @abstractmethod
    def update(self, user: User) -> None:
        pass

    @abstractmethod
    def delete(self, user: User) -> None:
        pass
