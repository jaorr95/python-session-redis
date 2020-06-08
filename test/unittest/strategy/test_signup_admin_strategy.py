from unittest import TestCase
from unittest.mock import patch, MagicMock
from app.src.strategy.signup_admin_strategy import SignupAdminStrategy
from app.src.models.admin import Admin
from app.src.exceptions.errors import UserExistsError, InvalidParametersError
from app.test.unittest.strategy.moks import MockQuery


class TestSignupAdminStrategy(TestCase):

	def setUp(self):
		self.mock_query = MockQuery()
		self.strategy =SignupAdminStrategy()
		self.data = dict(username="test", password="password")

	def tearDown(self):
		self.mock_query = None
		self.strategy = None
		self.data = None


	def test_success_signup(self):

		with patch("app.src.strategy.signup_admin_strategy.SignupAdminStrategy.validate_unique_username", 
			return_value=None):
			with patch("app.src.strategy.signup_admin_strategy.db"):
				admin = self.strategy.signup(self.data)

		self.assertIsInstance(admin, Admin)
		self.assertEqual(admin.username, self.data["username"])
		self.assertIsNotNone(admin.password)


	def test_error_signup(self):
		
		with self.assertRaises(InvalidParametersError):
			self.strategy.signup(dict())


	def test_success_validate_unique_username(self):

		admin = Admin(username="test")
		with patch("app.src.strategy.signup_admin_strategy.Admin.query", 
			new=self.mock_query):
			self.mock_query.first = MagicMock(return_value=None)
			void = self.strategy.validate_unique_username(admin)

		self.assertIsNone(void)

	def test_error_validate_unique_username(self):

		admin = Admin(username="test")
		with patch("app.src.strategy.signup_admin_strategy.Admin.query", 
			new=self.mock_query):

			self.mock_query.first = MagicMock(return_value=True)
			with self.assertRaises(UserExistsError):
				self.strategy.validate_unique_username(admin)