from unittest import TestCase
from unittest.mock import patch, MagicMock
from app.src.strategy.login_user_strategy import LoginUserStrategy
from app.src.exceptions.errors import InvalidParametersError
from app.src.models.user import User
from app.test.unittest.strategy.moks import MockQuery


class TestLoginUserStrategy(TestCase):

	def setUp(self):
		self.strategy = LoginUserStrategy()
		self.credentials = dict(email="test@user.com", password="testing1234")
		self.mock_query = MockQuery()

	def tearDown(self):
		self.strategy = None
		self.credentials = None
		self.mock_query = None


	def test_error_login(self):
		
		with self.assertRaises(InvalidParametersError):
			self.strategy.login(dict())


	def test_user_not_found_login(self):
		
		with patch("app.src.strategy.login_user_strategy.User.query", new=self.mock_query):
			
			self.mock_query.first = MagicMock(return_value=None)
			tokens = self.strategy.login(self.credentials)

		self.assertIsNone(tokens)


	def test_user_invalid_password_login(self):

		user = User(email=self.credentials["email"])

		with patch("app.src.models.user.Utils.hash_password", return_value=("salt","password")):
			user.password = self.credentials["password"]
		
		with patch("app.src.strategy.login_user_strategy.User.query", new=self.mock_query):
			
			self.mock_query.first = MagicMock(return_value=user)
			with patch("app.src.strategy.login_user_strategy.Utils.verify_password", 
				return_value=False):

				tokens = self.strategy.login(self.credentials)

		self.assertIsNone(tokens)


	def test_success_login(self):

		user = User(email=self.credentials["email"])

		with patch("app.src.models.user.Utils.hash_password", return_value=("salt","password")):
			user.password = self.credentials["password"]

		with patch("app.src.strategy.login_user_strategy.User.query", 
			new=self.mock_query):
			
			self.mock_query.first = MagicMock(return_value=user)
			with patch("app.src.strategy.login_user_strategy.Utils.verify_password", 
				return_value=True):
				
				with patch("app.src.strategy.login_user_strategy.Auth.generate_session_token",
					return_value=dict(refresh_id="refresh", token_id="token")):

					tokens = self.strategy.login(self.credentials)

		self.assertDictEqual(tokens, dict(refresh_id="refresh", token_id="token"))

