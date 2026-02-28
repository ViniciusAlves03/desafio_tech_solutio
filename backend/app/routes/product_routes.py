from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.di.di import container
from app.schemas.product_schema import product_schema, products_schema
from app.exceptions.api_exception_manager import APIExceptionManager

product_bp = Blueprint('product_bp', __name__)
product_service = container.get_product_service()

@product_bp.route('/products', methods=['POST'])
@jwt_required()
def create_product():
    try:
        data = product_schema.load(request.get_json())
        product_service.enqueue_create(data, int(get_jwt_identity()))
        return jsonify({"message": "Criação de produto enfileirada com sucesso."}), 202
    except Exception as error:
        api_error = APIExceptionManager.build(error)
        return make_response(jsonify(api_error.toJSON()), api_error.code)

@product_bp.route('/products', methods=['GET'])
@jwt_required()
def get_products():
    try:
        products = product_service.get_all()
        return jsonify(products_schema.dump(products)), 200
    except Exception as error:
        api_error = APIExceptionManager.build(error)
        return make_response(jsonify(api_error.toJSON()), api_error.code)

@product_bp.route('/products/<int:id>', methods=['GET'])
@jwt_required()
def get_product(id):
    try:
        product = product_service.get_by_id(id)
        return jsonify(product_schema.dump(product)), 200
    except Exception as error:
        api_error = APIExceptionManager.build(error)
        return make_response(jsonify(api_error.toJSON()), api_error.code)

@product_bp.route('/products/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_product(id):
    try:
        data = product_schema.load(request.get_json(), partial=True)
        product_service.enqueue_update(id, data, int(get_jwt_identity()))
        return jsonify({"message": "Atualização de produto enfileirada com sucesso."}), 202

    except Exception as error:
        api_error = APIExceptionManager.build(error)
        return make_response(jsonify(api_error.toJSON()), api_error.code)

@product_bp.route('/products/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_product(id):
    try:
        product_service.enqueue_delete(id, int(get_jwt_identity()))
        return jsonify({"message": "Exclusão de produto enfileirada com sucesso."}), 202
    except Exception as error:
        api_error = APIExceptionManager.build(error)
        return make_response(jsonify(api_error.toJSON()), api_error.code)
