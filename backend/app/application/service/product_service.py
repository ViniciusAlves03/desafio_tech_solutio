import json
from app.utils.redis_client import redis_conn
from app.application.port.product_repository_interface import IProductRepository
from app.application.domain.exception.domain_exceptions import NotFoundError, ForbiddenError, ValidationError

QUEUE_NAME = 'product_tasks'

class ProductService:
    def __init__(self, product_repository: IProductRepository):
        self.product_repository = product_repository

    def get_all(self):
        try:
            return self.product_repository.get_all()
        except Exception as error:
            raise error

    def get_by_id(self, product_id):
        try:
            product = self.product_repository.get_by_id(product_id)
            if not product:
                raise NotFoundError("Produto não encontrado.", f"O ID {product_id} não existe.")
            return product
        except Exception as error:
            raise error

    def enqueue_create(self, data, current_user_id):
        try:
            message = {
                "action": "create",
                "data": {
                    "name": data['name'],
                    "price": float(data['price']),
                    "brand": data['brand'],
                    "user_id": current_user_id
                }
            }
            redis_conn.rpush(QUEUE_NAME, json.dumps(message))
        except Exception as error:
            raise error

    def enqueue_update(self, product_id, data, current_user_id):
        try:
            product = self.get_by_id(product_id)

            if product.user_id != current_user_id:
                raise ForbiddenError("Acesso negado. Você só pode alterar seus próprios produtos.")

            update_data = {k: v for k, v in data.items() if k in ['name', 'price', 'brand']}
            if not update_data:
                raise ValidationError("Nenhum dado válido fornecido para atualização.")

            if 'price' in update_data:
                update_data['price'] = float(update_data['price'])

            message = {
                "action": "update",
                "product_id": product_id,
                "data": update_data
            }
            redis_conn.rpush(QUEUE_NAME, json.dumps(message))
        except Exception as error:
            raise error

    def enqueue_delete(self, product_id, current_user_id):
        try:
            product = self.get_by_id(product_id)

            if product.user_id != current_user_id:
                raise ForbiddenError("Acesso negado. Você só pode deletar seus próprios produtos.")

            message = {
                "action": "delete",
                "product_id": product_id
            }
            redis_conn.rpush(QUEUE_NAME, json.dumps(message))
        except Exception as error:
            raise error
