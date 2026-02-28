import json
from app.utils.redis_client import redis_conn
from app.repositories.product_repository import ProductRepository

QUEUE_NAME = 'product_tasks'

class ProductService:
    @staticmethod
    def enqueue_create(data, current_user_id):
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

    @staticmethod
    def enqueue_update(product_id, data, current_user_id):
        product = ProductRepository.get_by_id(product_id)
        if not product:
            return False, "Produto não encontrado."
        if product.user_id != current_user_id:
            return False, "Acesso negado. Você só pode alterar seus próprios produtos."

        update_data = {k: v for k, v in data.items() if k in ['name', 'price', 'brand']}
        if not update_data:
            return False, "Nenhum dado válido para atualizar."

        if 'price' in update_data:
            update_data['price'] = float(update_data['price'])

        message = {
            "action": "update",
            "product_id": product_id,
            "data": update_data
        }
        redis_conn.rpush(QUEUE_NAME, json.dumps(message))
        return True, None

    @staticmethod
    def enqueue_delete(product_id, current_user_id):
        product = ProductRepository.get_by_id(product_id)
        if not product:
            return False, "Produto não encontrado."
        if product.user_id != current_user_id:
            return False, "Acesso negado. Você só pode deletar seus próprios produtos."

        message = {
            "action": "delete",
            "product_id": product_id
        }
        redis_conn.rpush(QUEUE_NAME, json.dumps(message))
        return True, None
