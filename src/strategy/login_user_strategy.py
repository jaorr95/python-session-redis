from marshmallow.exceptions import ValidationError
from app.src.strategy.strategies import LoginStrategy
from app.src.schemas.user_schemas import UserLoginSchema, UserCreateSchema
from app.src.models.user import User
from app.src.common.utils import Utils
from app.src.common.auth import Auth
from app.src.exceptions.errors import InvalidParametersError


class LoginUserStrategy(LoginStrategy):

	def login(self, credentials: dict) -> dict:

		schema = UserLoginSchema()

		try:
			credentials = schema.load(credentials)
			storedUser = User.query.filter_by(email=credentials["email"]).first()
			
			if storedUser is None:
				return None

			isLogged = Utils.verify_password(
				storedUser.password[0], storedUser.password[1], credentials["password"]
				)
			data = UserCreateSchema().dump(storedUser)
			tokens = Auth.generate_session_token("USER", **data)
			
		except ValidationError as e:
			raise InvalidParametersError(e.data, e.messages, "Error occurred when trying to loggin user", e)	
			
		return tokens