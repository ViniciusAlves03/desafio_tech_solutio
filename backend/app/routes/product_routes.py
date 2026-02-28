from flask import Blueprint, request, jsonify
import json
from app.utils.db import db
from app.utils.redis_client import redis_conn
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.product_model import Product

product_bp = Blueprint('product_bp', __name__)

QUEUE_NAME = 'product_tasks'

@product_bp.route('/products', methods=['POST'])
@jwt_required()
def create_product():
    current_user_id = int(get_jwt_identity())
    data = request.get_json()

    if not data or not data.get('name') or not data.get('price') or not data.get('brand'):
        return jsonify({"error": "Dados incompletos. Informe 'name', 'price' e 'brand'."}), 400

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

    return jsonify({"message": "Criação de produto enfileirada com sucesso."}), 202

@product_bp.route('/products', methods=['GET'])
@jwt_required()
def get_products():
    products = Product.query.all()
    return jsonify([product.to_dict() for product in products]), 200

@product_bp.route('/products/<int:id>', methods=['GET'])
@jwt_required()
def get_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({"error": "Produto não encontrado."}), 404

    return jsonify(product.to_dict()), 200

@product_bp.route('/products/<int:id>', methods=['PATCH'])
@jwt_required()
def update_product(id):
    current_user_id = int(get_jwt_identity())

    product = Product.query.get(id)
    if not product:
        return jsonify({"error": "Produto não encontrado."}), 404

    if product.user_id != current_user_id:
        return jsonify({"error": "Acesso negado. Você só pode alterar seus próprios produtos."}), 403

    data = request.get_json()

    update_data = {}
    if 'name' in data:
        update_data['name'] = data['name']
    if 'price' in data:
        update_data['price'] = float(data['price'])
    if 'brand' in data:
        update_data['brand'] = data['brand']

    if not update_data:
        return jsonify({"error": "Nenhum dado válido para atualizar."}), 400

    message = {
        "action": "update",
        "product_id": id,
        "data": update_data
    }
    redis_conn.rpush(QUEUE_NAME, json.dumps(message))

    return jsonify({"message": "Atualização de produto enfileirada com sucesso."}), 202

@product_bp.route('/products/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_product(id):
    current_user_id = int(get_jwt_identity())

    product = Product.query.get(id)
    if not product:
        return jsonify({"error": "Produto não encontrado."}), 404

    if product.user_id != current_user_id:
        return jsonify({"error": "Acesso negado. Você só pode deletar seus próprios produtos."}), 403

    message = {
        "action": "delete",
        "product_id": id
    }
    redis_conn.rpush(QUEUE_NAME, json.dumps(message))

    return jsonify({"message": "Exclusão de produto enfileirada com sucesso."}), 202
