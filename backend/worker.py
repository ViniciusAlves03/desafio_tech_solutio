import base64
from decimal import Decimal
import json
import time
from app.utils.redis_client import redis_conn
from app.infrastructure.database.models.product_model import Product
from app.di.di import container

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
            print(f"[WORKER] Sucesso: Produto '{data['name']}' criado com imagem!")

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
                print(f"[WORKER] Sucesso: Produto ID {product_id} atualizado!")
            else:
                print(f"[WORKER - AVISO] Produto ID {product_id} não encontrado para atualização.")

        elif action == 'delete':
            product_id = message_data.get('product_id')

            product = product_repository.get_by_id(product_id)
            if product:
                product_repository.delete(product)
                print(f"[WORKER] Sucesso: Produto ID {product_id} deletado!")
            else:
                print(f"[WORKER - AVISO] Produto ID {product_id} não encontrado para exclusão.")

        else:
            print(f"[WORKER - ERRO] Ação desconhecida: {action}")

    except Exception as e:
        print(f"[WORKER - ERRO FATAL] Falha ao processar {action}: {str(e)}")


def run_worker():
    print("[WORKER] Iniciando o processador de fila...")
    time.sleep(5)

    print("[WORKER] Conectado! Aguardando novas mensagens no Redis...")
    while True:
        try:
            queue, message = redis_conn.blpop(QUEUE_NAME, timeout=0)
            if message:
                message_data = json.loads(message)
                print(f"\n[WORKER] Processando ação: {message_data.get('action').upper()}...")
                process_message(message_data)
        except Exception as e:
            print(f"[WORKER - ERRO DE CONEXÃO] {str(e)}")
            time.sleep(5)

if __name__ == '__main__':
    run_worker()
