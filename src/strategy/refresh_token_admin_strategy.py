from app.src.strategy.strategies import RefreshTokenStrategy
from app.src.schemas.admin_schemas import AdminCreateSchema
from app.src.models.admin import Admin
from app.src.common.auth import Auth


class RefreshTokenAdminStrategy(RefreshTokenStrategy):

	def refresh(self, refresh_token: str) -> dict:

		session = Auth.get_session(refresh_token)
		admin = Admin.query.filter_by(id=session["id"]).first()
		data = AdminCreateSchema().dump(admin)
		tokens = Auth.update_session(refresh_token, **data)
		
		return tokens