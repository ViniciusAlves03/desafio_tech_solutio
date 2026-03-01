import base64
import io
from flask import Blueprint, request, jsonify, make_response, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from
from app.di.di import container
from app.infrastructure.database.schemas.product_schema import product_schema, products_schema
from app.ui.exception.api_exception_manager import APIExceptionManager

product_bp = Blueprint('product_bp', __name__)
product_service = container.get_product_service()

@product_bp.route('/products', methods=['POST'])
@jwt_required()
@swag_from('../docs/swagger/products/create.yml')
def create_product():
    try:
        data = request.form.to_dict()
        valid_data = product_schema.load(data)
        image_file = request.files.get('image')
        if image_file:
            valid_data['image_base64'] = base64.b64encode(image_file.read()).decode('utf-8')
            valid_data['image_mime_type'] = image_file.mimetype

        product_service.enqueue_create(valid_data, int(get_jwt_identity()))
        return jsonify({"message": "Product creation queued successfully."}), 202
    except Exception as error:
        api_error = APIExceptionManager.build(error)
        return make_response(jsonify(api_error.toJSON()), api_error.code)

@product_bp.route('/products', methods=['GET'])
@jwt_required()
@swag_from('../docs/swagger/products/get_all.yml')
def get_products():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        name = request.args.get('name', type=str)
        brand = request.args.get('brand', type=str)

        result = product_service.get_all(page, per_page, name, brand)

        response_data = {
            "items": products_schema.dump(result["items"]),
            "metadata": {
                "total": result["total"],
                "page": result["page"],
                "per_page": result["per_page"],
                "total_pages": result["total_pages"]
            }
        }
        return jsonify(response_data), 200
    except Exception as error:
        api_error = APIExceptionManager.build(error)
        return make_response(jsonify(api_error.toJSON()), api_error.code)

@product_bp.route('/products/<int:id>', methods=['GET'])
@jwt_required()
@swag_from('../docs/swagger/products/get_by_id.yml')
def get_product(id):
    try:
        product = product_service.get_by_id(id)
        return jsonify(product_schema.dump(product)), 200
    except Exception as error:
        api_error = APIExceptionManager.build(error)
        return make_response(jsonify(api_error.toJSON()), api_error.code)

@product_bp.route('/products/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
@swag_from('../docs/swagger/products/update.yml')
def update_product(id):
    try:
        data = request.form.to_dict()
        valid_data = product_schema.load(data, partial=True)

        image_file = request.files.get('image')
        if image_file:
            valid_data['image_base64'] = base64.b64encode(image_file.read()).decode('utf-8')
            valid_data['image_mime_type'] = image_file.mimetype

        product_service.enqueue_update(id, valid_data, int(get_jwt_identity()))
        return jsonify({"message": "Product update queued successfully."}), 202
    except Exception as error:
        api_error = APIExceptionManager.build(error)
        return make_response(jsonify(api_error.toJSON()), api_error.code)

@product_bp.route('/products/<int:id>', methods=['DELETE'])
@jwt_required()
@swag_from('../docs/swagger/products/delete.yml')
def delete_product(id):
    try:
        product_service.enqueue_delete(id, int(get_jwt_identity()))
        return jsonify({"message": "Product deletion queued successfully."}), 202
    except Exception as error:
        api_error = APIExceptionManager.build(error)
        return make_response(jsonify(api_error.toJSON()), api_error.code)

@product_bp.route('/products/<int:id>/image', methods=['GET'])
@jwt_required()
@swag_from('../docs/swagger/products/get_image.yml')
def get_product_image(id):
    try:
        product = product_service.get_by_id(id)
        if not product or not product.image_data:
            return jsonify({"message": "Image not found."}), 404

        return send_file(
            io.BytesIO(product.image_data),
            mimetype=product.image_mime_type
        )
    except Exception as error:
        api_error = APIExceptionManager.build(error)
        return make_response(jsonify(api_error.toJSON()), api_error.code)
