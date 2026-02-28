from abc import ABC, abstractmethod

class IAuthService(ABC):
    @abstractmethod
    def login(self, login_input: str, password: str) -> dict:
        pass

    @abstractmethod
    def logout(self, jti: str) -> None:
        pass
