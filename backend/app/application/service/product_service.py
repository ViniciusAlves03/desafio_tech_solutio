import json
from app.utils.redis_client import redis_conn
from app.application.port.product_repository_interface import IProductRepository
from app.application.domain.exception.exceptions import NotFoundError, ForbiddenError, ValidationError

QUEUE_NAME = 'product_tasks'

class ProductService:
    def __init__(self, product_repository: IProductRepository):
        self.product_repository = product_repository

    def get_all(self, page=1, per_page=10, name=None, brand=None):
        try:
            products, total = self.product_repository.get_all(page, per_page, name, brand)

            total_pages = (total + per_page - 1) // per_page

            return {
                "items": products,
                "total": total,
                "page": page,
                "per_page": per_page,
                "total_pages": total_pages
            }
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
                    "price": str(data['price']),
                    "brand": data['brand'],
                    "quantity": int(data['quantity']),
                    "user_id": current_user_id,
                    "image_base64": data.get('image_base64'),
                    "image_mime_type": data.get('image_mime_type')
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

            update_data = {k: v for k, v in data.items() if k in ['name', 'price', 'brand', 'quantity', 'image_base64', 'image_mime_type']}
            if not update_data:
                raise ValidationError("Nenhum dado válido fornecido para atualização.")

            if 'price' in update_data:
                update_data['price'] = float(update_data['price'])
            if 'quantity' in update_data:
                update_data['quantity'] = int(update_data['quantity'])

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
