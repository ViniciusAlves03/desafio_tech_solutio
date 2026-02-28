from marshmallow import Schema, fields, validate, EXCLUDE

class UserSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(min=3))
    email = fields.Email(required=True, error_messages={"invalid": "E-mail inválido."})
    password = fields.Str(required=True, load_only=True, validate=validate.Length(min=6))

user_schema = UserSchema()
users_schema = UserSchema(many=True)
