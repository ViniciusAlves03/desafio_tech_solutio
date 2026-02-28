from app.models.user_model import User
from app.utils.db import db

class UserRepository:
    @staticmethod
    def create(user: User) -> User:
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def get_by_id(user_id: int) -> User:
        return User.query.get(user_id)

    @staticmethod
    def get_by_email(email: str) -> User:
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_by_username(username: str) -> User:
        return User.query.filter_by(username=username).first()

    @staticmethod
    def get_by_login_input(login_input: str) -> User:
        return User.query.filter(
            (User.email == login_input) | (User.username == login_input)
        ).first()

    @staticmethod
    def get_all() -> list[User]:
        return User.query.all()

    @staticmethod
    def update() -> None:
        db.session.commit()

    @staticmethod
    def delete(user: User) -> None:
        db.session.delete(user)
        db.session.commit()
