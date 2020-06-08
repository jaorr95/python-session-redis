from unittest import TestCase
from unittest.mock import patch, MagicMock
from app.src.strategy.login_admin_strategy import LoginAdminStrategy
from app.src.exceptions.errors import InvalidParametersError
from app.src.models.admin import Admin
from app.test.unittest.strategy.moks import MockQuery


class TestLoginAdminStrategy(TestCase):

	def setUp(self):
		self.strategy = LoginAdminStrategy()
		self.credentials = dict(username="test", password="testing1234")
		self.mock_query = MockQuery()

	def tearDown(self):
		self.strategy = None
		self.credentials = None
		self.mock_query = None

	def test_error_login(self):
		
		with self.assertRaises(InvalidParametersError):
			self.strategy.login(dict())


	def test_admin_not_found_login(self):
		
		with patch("app.src.strategy.login_admin_strategy.Admin.query", new=self.mock_query):
			
			self.mock_query.first = MagicMock(return_value=None)
			tokens = self.strategy.login(self.credentials)

		self.assertIsNone(tokens)


	def test_admin_invalid_password_login(self):

		admin = Admin(username=self.credentials["username"])

		with patch("app.src.models.admin.Utils.hash_password", return_value=("salt","password")):
			admin.password = self.credentials["password"]
		
		with patch("app.src.strategy.login_admin_strategy.Admin.query", new=self.mock_query):
			
			self.mock_query.first = MagicMock(return_value=admin)
			with patch("app.src.strategy.login_admin_strategy.Utils.verify_password", 
				return_value=False):

				tokens = self.strategy.login(self.credentials)

		self.assertIsNone(tokens)


	def test_success_login(self):

		admin = Admin(username=self.credentials["username"])

		with patch("app.src.models.admin.Utils.hash_password", return_value=("salt","password")):
			admin.password = self.credentials["password"]

		with patch("app.src.strategy.login_admin_strategy.Admin.query", 
			new=self.mock_query):
			
			self.mock_query.first = MagicMock(return_value=admin)
			with patch("app.src.strategy.login_admin_strategy.Utils.verify_password", 
				return_value=True):
				
				with patch("app.src.strategy.login_admin_strategy.Auth.generate_session_token",
					return_value=dict(refresh_id="refresh", token_id="token")):

					tokens = self.strategy.login(self.credentials)

		self.assertDictEqual(tokens, dict(refresh_id="refresh", token_id="token"))


