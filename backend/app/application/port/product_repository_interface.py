from abc import ABC, abstractmethod

from app.infrastructure.database.models import Product

class IProductRepository(ABC):
    @abstractmethod
    def create(self, product: Product) -> Product:
        pass

    @abstractmethod
    def get_by_id(self, product_id: int) -> Product:
        pass

    @abstractmethod
    def get_all(self, page: int, per_page: int, name: str = None, brand: str = None) -> tuple[list[Product], int]:
        pass

    @abstractmethod
    def update(self, product: Product) -> None:
        pass

    @abstractmethod
    def delete(self, product: Product) -> None:
        pass
