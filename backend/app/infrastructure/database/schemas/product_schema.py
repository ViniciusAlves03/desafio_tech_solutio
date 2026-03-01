from marshmallow import Schema, fields, validate, EXCLUDE
from app.utils.messages import Messages

class ProductSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Int(dump_only=True)

    name = fields.Str(
        required=True,
        validate=validate.Length(min=2, error=Messages.Validation.MIN_LENGTH_NAME)
    )
    price = fields.Decimal(
        required=True,
        as_string=True,
        validate=validate.Range(min=0.01, error=Messages.Validation.PRICE_GREATER_THAN_ZERO)
    )
    brand = fields.Str(
        required=True,
        validate=validate.Length(min=2)
    )
    quantity = fields.Int(
        required=True,
        validate=validate.Range(min=0, error=Messages.Validation.NEGATIVE_QUANTITY)
    )

    user_id = fields.Int(dump_only=True)
    image_url = fields.Method("get_image_url", dump_only=True)

    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    def get_image_url(self, obj):
        if getattr(obj, 'image_data', None):
            return f"/v1/products/{obj.id}/image"
        return None

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
