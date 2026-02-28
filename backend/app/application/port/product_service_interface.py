from abc import ABC, abstractmethod

class IProductService(ABC):
    @abstractmethod
    def get_all(self, page: int = 1, per_page: int = 10, name: str = None, brand: str = None) -> dict:
        pass

    @abstractmethod
    def get_by_id(self, product_id: int):
        pass

    @abstractmethod
    def enqueue_create(self, data: dict, current_user_id: int) -> None:
        pass

    @abstractmethod
    def enqueue_update(self, product_id: int, data: dict, current_user_id: int) -> None:
        pass

    @abstractmethod
    def enqueue_delete(self, product_id: int, current_user_id: int) -> None:
        pass
