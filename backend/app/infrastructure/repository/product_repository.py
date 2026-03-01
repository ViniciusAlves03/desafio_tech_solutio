from app.infrastructure.database.models.product_model import Product
from app.application.port.product_repository_interface import IProductRepository
from app.infrastructure.database.postgres.connection_postgres import ConnectionPostgres
from app.application.domain.exception.exceptions import ConflictError, RepositoryError
from app.utils.messages import Messages

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
                raise RepositoryError(Messages.Repository.ERR_SAVE_PRODUCT, str(error))

    def get_by_id(self, product_id: int) -> Product:
        with self.db.get_session() as session:
            try:
                return session.query(Product).filter(Product.id == product_id).first()
            except Exception as error:
                raise RepositoryError(Messages.Repository.ERR_GET_PRODUCT_ID, str(error))

    def get_all(self, page: int = 1, per_page: int = 10, name: str = None, brand: str = None) -> tuple[list[Product], int]:
        with self.db.get_session() as session:
            try:
                query = session.query(Product)
                if name:
                    query = query.filter(Product.name.ilike(f"%{name}%"))
                if brand:
                    query = query.filter(Product.brand.ilike(f"%{brand}%"))

                total = query.count()

                products = query.offset((page - 1) * per_page).limit(per_page).all()

                return products, total
            except Exception as error:
                raise RepositoryError(Messages.Repository.ERR_GET_PRODUCTS, str(error))

    def update(self, product: Product) -> None:
        with self.db.get_session() as session:
            try:
                session.merge(product)
                session.commit()
            except Exception as error:
                session.rollback()
                raise RepositoryError(Messages.Repository.ERR_UPDATE_PRODUCT, str(error))

    def delete(self, product: Product) -> None:
        with self.db.get_session() as session:
            try:
                merged_product = session.merge(product)
                session.delete(merged_product)
                session.commit()
            except Exception as error:
                session.rollback()
                raise RepositoryError(Messages.Repository.ERR_DELETE_PRODUCT, str(error))
