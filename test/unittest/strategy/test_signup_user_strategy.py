from unittest import TestCase
from unittest.mock import patch, MagicMock
from app.src.strategy.signup_user_strategy import SignupUserStrategy
from app.src.models.user import User
from app.src.exceptions.errors import UserExistsError, InvalidParametersError
from app.test.unittest.strategy.moks import MockQuery


class TestSignupUserStrategy(TestCase):

	def setUp(self):
		self.mock_query = MockQuery()
		self.strategy =SignupUserStrategy()
		self.data = dict(email="test@user.com", password="password", name="test", lastname="testing")

	def tearDown(self):
		self.mock_query = None
		self.strategy = None
		self.data = None


	def test_success_signup(self):

		with patch("app.src.strategy.signup_user_strategy.SignupUserStrategy.validate_unique_email", 
			return_value=None):
			with patch("app.src.strategy.signup_user_strategy.db"):
				user = self.strategy.signup(self.data)

		self.assertIsInstance(user, User)
		self.assertEqual(user.email, self.data["email"])
		self.assertEqual(user.name, self.data["name"])
		self.assertEqual(user.lastname, self.data["lastname"])
		self.assertIsNotNone(user.password)


	def test_error_signup(self):
		
		with self.assertRaises(InvalidParametersError):
			self.strategy.signup(dict())


	def test_success_validate_unique_email(self):

		user = User(email="test@user.com")
		with patch("app.src.strategy.signup_user_strategy.User.query", 
			new=self.mock_query):
			self.mock_query.first = MagicMock(return_value=None)
			void = self.strategy.validate_unique_email(user)

		self.assertIsNone(void)

	def test_error_validate_unique_email(self):

		user = User(email="test@user.com")
		with patch("app.src.strategy.signup_user_strategy.User.query", 
			new=self.mock_query):

			self.mock_query.first = MagicMock(return_value=True)
			with self.assertRaises(UserExistsError):
				self.strategy.validate_unique_email(user)