from app.repositories.user_repository import UserRepository
from app.repositories.product_repository import ProductRepository

from app.services.auth_service import AuthService
from app.services.product_service import ProductService
from app.services.user_service import UserService

from app.port.auth_service_interface import IAuthService
from app.port.product_service_interface import IProductService
from app.port.user_service_interface import IUserService

class DIContainer:
    def __init__(self):
        self._user_repository = UserRepository()
        self._product_repository = ProductRepository()
        self._auth_service = AuthService(user_repository=self._user_repository)
        self._product_service = ProductService(product_repository=self._product_repository)
        self._user_service = UserService(user_repository=self._user_repository)

    def get_auth_service(self) -> IAuthService:
        return self._auth_service

    def get_product_service(self) -> IProductService:
        return self._product_service

    def get_user_service(self) -> IUserService:
        return self._user_service

container = DIContainer()
