import base64
from decimal import Decimal
import json
import time
from app.infrastructure.redis import redis_conn
from app.infrastructure.database.models import Product
from app.di import container

QUEUE_NAME = 'product_tasks'

def process_message(message_data):
    action = message_data.get('action')
    product_repository = container._product_repository

    try:
        if action == 'create':
            data = message_data.get('data')
            new_product = Product(
                name=data['name'],
                price=Decimal(data['price']),
                brand=data['brand'],
                quantity=data['quantity'],
                user_id=data['user_id']
            )

            if data.get('image_base64'):
                new_product.image_data = base64.b64decode(data['image_base64'])
                new_product.image_mime_type = data.get('image_mime_type')

            product_repository.create(new_product)
            print(f"[WORKER] Success: Product '{data['name']}' created")

        elif action == 'update':
            product_id = message_data.get('product_id')
            data = message_data.get('data')

            product = product_repository.get_by_id(product_id)
            if product:
                if 'name' in data: product.name = data['name']
                if 'price' in data: product.price = Decimal(data['price'])
                if 'brand' in data: product.brand = data['brand']
                if 'quantity' in data: product.quantity = data['quantity']

                if 'image_base64' in data:
                    product.image_data = base64.b64decode(data['image_base64'])
                    product.image_mime_type = data.get('image_mime_type')

                product_repository.update(product)
                print(f"[WORKER] Success: Product ID {product_id} updated!")
            else:
                print(f"[WORKER - WARNING] Product ID {product_id} not found for update.")

        elif action == 'delete':
            product_id = message_data.get('product_id')

            product = product_repository.get_by_id(product_id)
            if product:
                product_repository.delete(product)
                print(f"[WORKER] Success: Product ID {product_id} deleted!")
            else:
                print(f"[WORKER - WARNING] Product ID {product_id} not found for deletion.")

        else:
            print(f"[WORKER - ERROR] Unknown action: {action}")

    except Exception as e:
        print(f"[WORKER - FATAL ERROR] Failed to process {action}: {str(e)}")


def run_worker():
    print("[WORKER] Starting queue processor")
    time.sleep(5)

    print("[WORKER] Connected! Waiting for new messages in Redis")
    while True:
        try:
            queue, message = redis_conn.blpop(QUEUE_NAME, timeout=0)
            if message:
                message_data = json.loads(message)
                print(f"\n[WORKER] Processing action: {message_data.get('action').upper()}...")
                process_message(message_data)
        except Exception as e:
            print(f"[WORKER - CONNECTION ERROR] {str(e)}")
            time.sleep(5)

if __name__ == '__main__':
    run_worker()
