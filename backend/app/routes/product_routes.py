from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.product_service import ProductService
from app.repositories.product_repository import ProductRepository

product_bp = Blueprint('product_bp', __name__)

@product_bp.route('/products', methods=['POST'])
@jwt_required()
def create_product():
    data = request.get_json()
    if not data or not all(k in data for k in ('name', 'price', 'brand')):
        return jsonify({"error": "Dados incompletos. Informe 'name', 'price' e 'brand'."}), 400

    ProductService.enqueue_create(data, int(get_jwt_identity()))
    return jsonify({"message": "Criação de produto enfileirada com sucesso."}), 202

@product_bp.route('/products', methods=['GET'])
@jwt_required()
def get_products():
    products = ProductRepository.get_all()
    return jsonify([product.to_dict() for product in products]), 200

@product_bp.route('/products/<int:id>', methods=['GET'])
@jwt_required()
def get_product(id):
    product = ProductRepository.get_by_id(id)
    if not product:
        return jsonify({"error": "Produto não encontrado."}), 404
    return jsonify(product.to_dict()), 200

@product_bp.route('/products/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_product(id):
    success, error = ProductService.enqueue_update(id, request.get_json(), int(get_jwt_identity()))
    if error:
        return jsonify({"error": error}), 400 if error == "Nenhum dado válido para atualizar." else (403 if "Acesso negado" in error else 404)

    return jsonify({"message": "Atualização de produto enfileirada com sucesso."}), 202

@product_bp.route('/products/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_product(id):
    success, error = ProductService.enqueue_delete(id, int(get_jwt_identity()))
    if error:
        return jsonify({"error": error}), 403 if "Acesso negado" in error else 404

    return jsonify({"message": "Exclusão de produto enfileirada com sucesso."}), 202
