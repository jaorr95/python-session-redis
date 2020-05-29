from marshmallow.exceptions import ValidationError
from app.src.strategy.strategies import SignupStrategy
from app.src.schemas.user_schemas import UserCreateSchema
from app.config.config import db
from app.src.exceptions.errors import InvalidParametersError, UserExistsError
from app.src.models.user import User


class SignupUserStrategy(SignupStrategy):

	def signup(self, data: dict) -> User:

		schema = UserCreateSchema()
		try:
			user = schema.load(data)
			self.validate_unique_email(user)
			db.session.add(user)
			db.session.commit()
		except ValidationError as e:
			raise InvalidParametersError(e, e.data, e.messages, "Error occurred when trying to create new user")
		return user


	def validate_unique_email(self, user):

		exists = User.query.filter_by(email=user.email).first()

		if exists:
			raise UserExistsError(
				user.email, "email: {0}, is not unique".format(user.email), 
				"Error occurred when trying to create new user")
		


