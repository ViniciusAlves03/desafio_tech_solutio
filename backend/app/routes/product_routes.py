from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.repositories.product_repository import ProductRepository
from app.services.product_service import ProductService
from app.exceptions.exceptions import ValidationException

product_bp = Blueprint('product_bp', __name__)

product_repo = ProductRepository()
product_service = ProductService(product_repository=product_repo)

@product_bp.route('/products', methods=['POST'])
@jwt_required()
def create_product():
    data = request.get_json()
    if not data or not all(k in data for k in ('name', 'price', 'brand')):
        raise ValidationException("Dados incompletos. Informe 'name', 'price' e 'brand'.")

    product_service.enqueue_create(data, int(get_jwt_identity()))
    return jsonify({"message": "Criação de produto enfileirada com sucesso."}), 202

@product_bp.route('/products', methods=['GET'])
@jwt_required()
def get_products():
    products = product_service.get_all()
    return jsonify([product.to_dict() for product in products]), 200

@product_bp.route('/products/<int:id>', methods=['GET'])
@jwt_required()
def get_product(id):
    product = product_service.get_by_id(id)
    return jsonify(product.to_dict()), 200

@product_bp.route('/products/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_product(id):
    product_service.enqueue_update(id, request.get_json(), int(get_jwt_identity()))
    return jsonify({"message": "Atualização de produto enfileirada com sucesso."}), 202

@product_bp.route('/products/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_product(id):
    product_service.enqueue_delete(id, int(get_jwt_identity()))
    return jsonify({"message": "Exclusão de produto enfileirada com sucesso."}), 202
