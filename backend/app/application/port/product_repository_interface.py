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
    def get_all(self, page=1, per_page=10, name=None, brand=None, sort_by="id", sort_order="asc"):
        pass

    @abstractmethod
    def update(self, product: Product) -> None:
        pass

    @abstractmethod
    def delete(self, product: Product) -> None:
        pass
