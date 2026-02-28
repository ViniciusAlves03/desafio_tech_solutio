from app.utils.db import db
from app.application.port.product_repository_interface import IProductRepository
from app.application.domain.exception.domain_exceptions import ConflictError, RepositoryError
from app.infrastructure.database.models.product_model import Product

class ProductRepository(IProductRepository):

    def create(self, product):
        try:
            db.session.add(product)
            db.session.commit()
            return product
        except Exception as error:
            db.session.rollback()
            raise RepositoryError("Erro ao salvar o produto no banco de dados.", str(error))

    def get_by_id(self, product_id: int):
        try:
            return Product.query.get(product_id)
        except Exception as error:
            raise RepositoryError("Erro ao buscar o produto por ID.", str(error))

    def get_all(self):
        try:
            return Product.query.all()
        except Exception as error:
            raise RepositoryError("Erro ao listar os produtos.", str(error))

    def update(self):
        try:
            db.session.commit()
        except Exception as error:
            db.session.rollback()
            raise RepositoryError("Erro ao atualizar o produto no banco de dados.", str(error))

    def delete(self, product):
        try:
            db.session.delete(product)
            db.session.commit()
        except Exception as error:
            db.session.rollback()
            raise RepositoryError("Erro ao deletar o produto no banco de dados.", str(error))
