from marshmallow import fields, EXCLUDE, Schema
from app.config.config import ma
from app.src.models.user import User


class UserCreateSchema(ma.ModelSchema):

	class Meta:

		model = User
		unknown = EXCLUDE
		exclude = ('_salt','_password')

	email = fields.Email(required=True)
	password = fields.String(required=True, load_only=True)


class UserLoginSchema(Schema):

	class Meta:
		
		unknown = EXCLUDE

	email = fields.Email(required=True)
	password = fields.String(required=True)