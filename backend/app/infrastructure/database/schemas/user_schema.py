from marshmallow import Schema, fields, validate, EXCLUDE
from app.utils.messages import Messages

class UserSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Int(dump_only=True)
    username = fields.Str(
        required=True,
        validate=validate.Length(min=3, error=Messages.Validation.MIN_LENGTH_USERNAME)
    )
    email = fields.Email(
        required=True,
        error_messages={"invalid": Messages.Validation.INVALID_EMAIL}
    )
    password = fields.Str(
        required=True,
        load_only=True,
        validate=validate.Length(min=6, error=Messages.Validation.MIN_LENGTH_PASSWORD)
    )

user_schema = UserSchema()
users_schema = UserSchema(many=True)
