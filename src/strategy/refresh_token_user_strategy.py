from app.src.strategy.strategies import RefreshTokenStrategy
from app.src.schemas.user_schemas import UserCreateSchema
from app.src.models.user import User
from app.src.common.auth import Auth


class RefreshTokenUserStrategy(RefreshTokenStrategy):

	def refresh(self, refresh_token: str) -> dict:

		session = Auth.get_session(refresh_token)
		user = User.query.filter_by(id=session["id"]).first()
		data = UserCreateSchema().dump(user)
		tokens = Auth.update_session(refresh_token, **data)
		
		return tokens