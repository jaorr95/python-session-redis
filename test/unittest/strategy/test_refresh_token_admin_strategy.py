from unittest import TestCase
from unittest.mock import patch, MagicMock
from app.src.strategy.refresh_token_admin_strategy import RefreshTokenAdminStrategy
from app.src.models.admin import Admin
from app.test.unittest.strategy.moks import MockQuery


class TestRefreshTokenAdminStrategy(TestCase):

	def setUp(self):
		self.strategy = RefreshTokenAdminStrategy()
		self.mock_query = MockQuery()

	def tearDown(self):
		self.strategy = None
		self.mock_query = None
		

	def test_success_refresh_token(self):

		admin = Admin(username="test")

		with patch("app.src.models.admin.Utils.hash_password", return_value=("salt","password")):
			admin.password = "password"
		
		with patch("app.src.strategy.refresh_token_admin_strategy.Auth.get_session", 
			return_value=dict(id=1)):

			with patch("app.src.strategy.refresh_token_admin_strategy.Admin.query", 
				new=self.mock_query):

				with patch("app.src.strategy.refresh_token_admin_strategy.Auth.update_session",
					return_value=dict(refresh_token="refresh", token_id="token")):

				
					self.mock_query.first = MagicMock(return_value=admin)
					tokens = self.strategy.refresh("refresh id")

		self.assertDictEqual(tokens, dict(refresh_token="refresh", token_id="token"))