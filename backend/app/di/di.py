from app.infrastructure.database.postgres import ConnectionPostgres

from app.infrastructure.repository import (UserRepository,
                                           ProductRepository)

from app.application.service import (AuthService,
                                     ProductService,
                                     UserService)

from app.application.port import (IAuthService,
                                  IProductService,
                                  IUserService)

class DIContainer:
    def __init__(self):
        self._db_connection = ConnectionPostgres()
        self._user_repository = UserRepository(db_connection=self._db_connection)
        self._product_repository = ProductRepository(db_connection=self._db_connection)
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
