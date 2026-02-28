from app.infrastructure.database.models.product_model import Product
from app.application.port.product_repository_interface import IProductRepository
from app.infrastructure.database.postgres.connection_postgres import ConnectionPostgres
from app.application.domain.exception.domain_exceptions import ConflictError, RepositoryError

class ProductRepository(IProductRepository):
    def __init__(self, db_connection: ConnectionPostgres):
        self.db = db_connection

    def create(self, product: Product) -> Product:
        with self.db.get_session() as session:
            try:
                session.add(product)
                session.commit()
                session.refresh(product)
                return product
            except Exception as error:
                session.rollback()
                raise RepositoryError("Erro ao salvar o produto no banco de dados.", str(error))

    def get_by_id(self, product_id: int) -> Product:
        with self.db.get_session() as session:
            try:
                return session.query(Product).filter(Product.id == product_id).first()
            except Exception as error:
                raise RepositoryError("Erro ao buscar o produto por ID.", str(error))

    def get_all(self) -> list[Product]:
        with self.db.get_session() as session:
            try:
                return session.query(Product).all()
            except Exception as error:
                raise RepositoryError("Erro ao listar os produtos.", str(error))

    def update(self, product: Product) -> None:
        with self.db.get_session() as session:
            try:
                session.merge(product)
                session.commit()
            except Exception as error:
                session.rollback()
                raise RepositoryError("Erro ao atualizar o produto no banco de dados.", str(error))

    def delete(self, product: Product) -> None:
        with self.db.get_session() as session:
            try:
                merged_product = session.merge(product)
                session.delete(merged_product)
                session.commit()
            except Exception as error:
                session.rollback()
                raise RepositoryError("Erro ao deletar o produto no banco de dados.", str(error))
