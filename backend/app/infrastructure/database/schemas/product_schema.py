from marshmallow import Schema, fields, validate, EXCLUDE

class ProductSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=2, error="O nome deve ter pelo menos 2 caracteres."))
    price = fields.Decimal(required=True, as_string=True, validate=validate.Range(min=0.01))
    brand = fields.Str(required=True, validate=validate.Length(min=2))
    quantity = fields.Int(required=True, validate=validate.Range(min=0, error="A quantidade não pode ser negativa."))
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
