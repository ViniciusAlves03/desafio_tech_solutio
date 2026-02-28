from flask import Blueprint, request, jsonify
from app.utils.db import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.product_model import Product

product_bp = Blueprint('product_bp', __name__)

@product_bp.route('/products', methods=['POST'])
@jwt_required()
def create_product():
    current_user_id = int(get_jwt_identity())
    data = request.get_json()

    if not data or not data.get('name') or not data.get('price') or not data.get('brand'):
        return jsonify({"error": "Dados incompletos. Informe 'name', 'price' e 'brand'."}), 400

    new_product = Product(
        name=data['name'],
        price=float(data['price']),
        brand=data['brand'],
        user_id=current_user_id
    )

    db.session.add(new_product)
    db.session.commit()

    return jsonify(new_product.to_dict()), 201

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

    if 'name' in data:
        product.name = data['name']
    if 'price' in data:
        product.price = float(data['price'])
    if 'brand' in data:
        product.brand = data['brand']

    db.session.commit()
    return jsonify(product.to_dict()), 200

@product_bp.route('/products/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_product(id):
    current_user_id = int(get_jwt_identity())
    product = Product.query.get(id)
    if not product:
        return jsonify({"error": "Produto não encontrado."}), 404

    if product.user_id != current_user_id:
        return jsonify({"error": "Acesso negado. Você só pode deletar seus próprios produtos."}), 403

    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Produto deletado com sucesso."}), 200
