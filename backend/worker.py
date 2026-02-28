import json
import time
from app.app import create_app
from app.utils.db import db
from app.utils.redis_client import redis_conn
from app.models.product_model import Product
from app.repositories.product_repository import ProductRepository

QUEUE_NAME = 'product_tasks'

def process_message(message_data):
    action = message_data.get('action')

    try:
        if action == 'create':
            data = message_data.get('data')
            new_product = Product(
                name=data['name'],
                price=data['price'],
                brand=data['brand'],
                user_id=data['user_id']
            )
            ProductRepository.create(new_product)
            print(f"[WORKER] Sucesso: Produto '{data['name']}' criado no banco!")

        elif action == 'update':
            product_id = message_data.get('product_id')
            data = message_data.get('data')

            product = ProductRepository.get_by_id(product_id)
            if product:
                if 'name' in data:
                    product.name = data['name']
                if 'price' in data:
                    product.price = data['price']
                if 'brand' in data:
                    product.brand = data['brand']

                ProductRepository.update()
                print(f"[WORKER] Sucesso: Produto ID {product_id} atualizado!")
            else:
                print(f"[WORKER - AVISO] Produto ID {product_id} não encontrado para atualização.")

        elif action == 'delete':
            product_id = message_data.get('product_id')

            product = ProductRepository.get_by_id(product_id)
            if product:
                ProductRepository.delete(product)
                print(f"[WORKER] Sucesso: Produto ID {product_id} deletado!")
            else:
                print(f"[WORKER - AVISO] Produto ID {product_id} não encontrado para exclusão.")

        else:
            print(f"[WORKER - ERRO] Ação desconhecida: {action}")

    except Exception as e:
        db.session.rollback()
        print(f"[WORKER - ERRO FATAL] Falha ao processar {action}: {str(e)}")


def run_worker():
    print("[WORKER] Iniciando o processador de fila...")
    app = create_app()
    with app.app_context():
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
