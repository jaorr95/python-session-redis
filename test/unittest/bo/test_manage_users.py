from unittest import TestCase
from unittest.mock import patch, MagicMock
from app.test.unittest.bo.mocks import MockSignupUserStrategy, MockSignupAdminStrategy
from app.test.unittest.bo.mocks import MockLoginUserStrategy, MockLoginAdminStrategy
from app.test.unittest.bo.mocks import MockRefreshTokenUserStrategy, MockRefreshTokenAdminStrategy
from app.src.bo.manage_users import ManageUser
from app.src.models.admin import Admin
from app.src.models.user import User
from app.src.exceptions.errors import AuthenticationError


class TestManageLogin(TestCase):

	def setUp(self):
		self.admin_strategy = MockLoginAdminStrategy()
		self.user_strategy = MockLoginUserStrategy()
		self.manage = ManageUser()

	def tearDown(self):
		self.admin_strategy = None
		self.user_strategy = None
		self.manage = None

	def test_success_admin_login(self):

		mock_return = dict(token_id="admin token", refresh_token="admin refresh token")
		self.admin_strategy.login = MagicMock(return_value = mock_return)
		tokens = self.manage.login(self.admin_strategy, dict())
		self.assertDictEqual(tokens, mock_return)

		

	def test_success_user_login(self):

		mock_return = dict(token_id="user token", refresh_token="user refresh token")
		self.user_strategy.login = MagicMock(return_value = mock_return)
		tokens = self.manage.login(self.user_strategy, dict())
		self.assertDictEqual(tokens, mock_return)

	def test_error_login(self):
		
		self.user_strategy.login = MagicMock(return_value = None)
		with self.assertRaises(AuthenticationError):
			self.manage.login(self.user_strategy, dict())

class TestManageSignup(TestCase):

	def setUp(self):
		self.admin_strategy = MockSignupAdminStrategy()
		self.user_strategy = MockSignupUserStrategy()
		self.manage = ManageUser()

	def tearDown(self):
		self.admin_strategy = None
		self.user_strategy = None
		self.manage = None

	def test_success_admin_signup(self):

		self.admin_strategy.signup = MagicMock(return_value=Admin())
		admin = self.manage.signup(self.admin_strategy, dict())
		self.assertIsInstance(admin, Admin)

	def test_success_user_signup(self):

		self.user_strategy.signup = MagicMock(return_value=User())
		user = self.manage.signup(self.user_strategy, dict())
		self.assertIsInstance(user, User)

class TestManageRefresh(TestCase):

	def setUp(self):
		self.admin_strategy = MockRefreshTokenAdminStrategy()
		self.user_strategy = MockRefreshTokenUserStrategy()
		self.manage = ManageUser()

	def tearDown(self):
		self.admin_strategy = None
		self.user_strategy = None
		self.manage = None
	

	def test_success_admin_refresh(self):
		
		mock_return = dict(token_id="admin token", refresh_token="admin refresh token")
		self.admin_strategy.refresh = MagicMock(return_value=mock_return)
		tokens = self.manage.refresh(self.admin_strategy, "refresh token")
		self.assertDictEqual(tokens, mock_return)

	def test_success_user_refresh(self):
		
		mock_return = dict(token_id="user token", refresh_token="user refresh token")
		self.user_strategy.refresh = MagicMock(return_value=mock_return)
		tokens = self.manage.refresh(self.user_strategy, "refresh token")
		self.assertDictEqual(tokens, mock_return)