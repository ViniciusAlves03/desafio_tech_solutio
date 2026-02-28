from marshmallow import Schema, fields, validate, EXCLUDE

class ProductSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=2, error="O nome deve ter pelo menos 2 caracteres."))
    price = fields.Float(required=True, validate=validate.Range(min=0.01, error="O preço deve ser maior que zero."))
    brand = fields.Str(required=True, validate=validate.Length(min=2))
    user_id = fields.Int(dump_only=True)

    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
