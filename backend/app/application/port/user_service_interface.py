from abc import ABC, abstractmethod

class IUserService(ABC):
    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_by_id(self, user_id: int):
        pass

    @abstractmethod
    def create_user(self, data: dict):
        pass

    @abstractmethod
    def update_user(self, user_id: int, current_user_id: int, data: dict):
        pass

    @abstractmethod
    def delete_user(self, user_id: int, current_user_id: int) -> None:
        pass
