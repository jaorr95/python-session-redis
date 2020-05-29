from marshmallow import EXCLUDE, fields, Schema
from app.config.config import ma
from app.src.models.admin import Admin


class AdminCreateSchema(ma.ModelSchema):

	class Meta:

		model = Admin
		unknown = EXCLUDE
		exclude = ('_salt','_password')

	password = fields.String(required=True, load_only=True)


class AdminLoginSchema(Schema):

	class Meta:
		
		unknown = EXCLUDE

	username = fields.String(required=True)
	password = fields.String(required=True)
