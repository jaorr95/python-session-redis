from marshmallow.exceptions import ValidationError
from app.src.strategy.strategies import LoginStrategy
from app.src.schemas.admin_schemas import AdminLoginSchema, AdminCreateSchema
from app.src.models.admin import Admin
from app.src.common.utils import Utils
from app.src.common.auth import Auth
from app.src.exceptions.errors import InvalidParametersError


class LoginAdminStrategy(LoginStrategy):

	def login(self, credentials: dict) -> dict:

		schema = AdminLoginSchema()
		
		try:
			credentials = schema.load(credentials)
			storedAdmin = Admin.query.filter_by(username=credentials["username"]).first()
			
			if storedAdmin is None:
				return None

			isLogged = Utils.verify_password(
				storedAdmin.password[0], storedAdmin.password[1], credentials["password"]
				)
			data = AdminCreateSchema().dump(storedAdmin)
			tokens = Auth.generate_session_token("ADMIN", **data)

		except ValidationError as e:
			raise InvalidParametersError(e.data, e.messages, "Error occurred when trying to loggin admin", e)
			
		return tokens