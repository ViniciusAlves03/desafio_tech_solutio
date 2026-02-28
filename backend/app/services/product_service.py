import json
from app.utils.redis_client import redis_conn
from app.port.product_repository_interface import IProductRepository
from app.port.product_service_interface import IProductService
from app.exceptions.exceptions import NotFoundException, ForbiddenException, ValidationException

QUEUE_NAME = 'product_tasks'

class ProductService(IProductService):
    def __init__(self, product_repository: IProductRepository):
        self.product_repository = product_repository

    def get_all(self):
        return self.product_repository.get_all()

    def get_by_id(self, product_id):
        product = self.product_repository.get_by_id(product_id)
        if not product:
            raise NotFoundException("Produto não encontrado.")
        return product

    def enqueue_create(self, data, current_user_id):
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

    def enqueue_update(self, product_id, data, current_user_id):
        product = self.get_by_id(product_id)

        if product.user_id != current_user_id:
            raise ForbiddenException("Acesso negado. Você só pode alterar seus próprios produtos.")

        update_data = {k: v for k, v in data.items() if k in ['name', 'price', 'brand']}
        if not update_data:
            raise ValidationException("Nenhum dado válido para atualizar.")

        if 'price' in update_data:
            update_data['price'] = float(update_data['price'])

        message = {
            "action": "update",
            "product_id": product_id,
            "data": update_data
        }
        redis_conn.rpush(QUEUE_NAME, json.dumps(message))

    def enqueue_delete(self, product_id, current_user_id):
        product = self.get_by_id(product_id)

        if product.user_id != current_user_id:
            raise ForbiddenException("Acesso negado. Você só pode deletar seus próprios produtos.")

        message = {
            "action": "delete",
            "product_id": product_id
        }
        redis_conn.rpush(QUEUE_NAME, json.dumps(message))
