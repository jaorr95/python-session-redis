from unittest import TestCase
from unittest.mock import patch, MagicMock
from app.src.strategy.refresh_token_user_strategy import RefreshTokenUserStrategy
from app.src.models.user import User
from app.test.unittest.strategy.moks import MockQuery


class TestRefreshTokenUserStrategy(TestCase):

	def setUp(self):
		self.strategy = RefreshTokenUserStrategy()
		self.mock_query = MockQuery()

	def tearDown(self):
		self.strategy = None
		self.mock_query = None
		

	def test_success_refresh_token(self):

		user = User(email="test@user.com")

		with patch("app.src.models.user.Utils.hash_password", return_value=("salt","password")):
			user.password = "password"
		
		with patch("app.src.strategy.refresh_token_user_strategy.Auth.get_session", 
			return_value=dict(id=1)):

			with patch("app.src.strategy.refresh_token_user_strategy.User.query", 
				new=self.mock_query):

				with patch("app.src.strategy.refresh_token_user_strategy.Auth.update_session",
					return_value=dict(refresh_token="refresh", token_id="token")):

				
					self.mock_query.first = MagicMock(return_value=user)
					tokens = self.strategy.refresh("refresh id")

		self.assertDictEqual(tokens, dict(refresh_token="refresh", token_id="token"))