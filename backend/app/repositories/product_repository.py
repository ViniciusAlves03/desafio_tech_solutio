from app.models.product_model import Product
from app.utils.db import db

class ProductRepository:
    @staticmethod
    def create(product: Product) -> Product:
        db.session.add(product)
        db.session.commit()
        return product

    @staticmethod
    def get_by_id(product_id: int) -> Product:
        return Product.query.get(product_id)

    @staticmethod
    def get_all() -> list[Product]:
        return Product.query.all()

    @staticmethod
    def update() -> None:
        db.session.commit()

    @staticmethod
    def delete(product: Product) -> None:
        db.session.delete(product)
        db.session.commit()
