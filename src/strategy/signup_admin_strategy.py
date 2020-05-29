from marshmallow.exceptions import ValidationError
from app.src.strategy.strategies import SignupStrategy
from app.src.schemas.admin_schemas import AdminCreateSchema
from app.config.config import db
from app.src.models.admin import Admin
from app.src.exceptions.errors import UserExistsError, InvalidParametersError


class SignupAdminStrategy(SignupStrategy):

	def signup(self, data: dict) -> Admin:
		
		schema = AdminCreateSchema()
		try:
		
			admin = schema.load(data)
			self.validate_unique_username()
			db.session.add(admin)
			db.session.commit()
		except ValidationError as e:
			raise InvalidParametersError(e.data, e.messages, 
				"Error occurred when trying to create new admin", e)
		
		return admin

	def validate_unique_username(self, admin):

		exists = Admin.query.filter_by(username=admin.username).first()

		if exists:
			raise UserExistsError(
				admin.username, "username: {0}, is not unique".format(admin.username), 
				"Error occurred when trying to create a new administrator")
