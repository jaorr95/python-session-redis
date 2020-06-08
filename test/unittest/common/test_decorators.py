from unittest import TestCase
from unittest.mock import patch
from app.src.common.decorators import is_authenticated, refresh_token
from app.src.exceptions.errors import InvalidTokenError

class MockUtils:

	@staticmethod
	def response(*, status=200, data=[], message=""):
		return dict(status=status, data=data, message=message)

	@staticmethod
	def request_role():
		return "test"


class TestDecorator(TestCase):

	def setUp(self):
		self.bearer_token = "Bearer token_success"
		self.func = lambda :True

	def tearDown(self):
		self.bearer_token = None
		self.func = None


	def test_success_is_authenticated(self):

		with patch("app.src.common.decorators.request") as mock_request:

			mock_request.headers = dict(Authorization=self.bearer_token)
			with patch("app.src.common.decorators.Utils", new_callable=MockUtils):

				with patch("app.src.common.decorators.Auth.token_decode", return_value=dict(token="session token")):

					with patch("app.src.common.decorators.Auth.session_exists", return_value=True):

						success = is_authenticated(self.func)()
						
		self.assertTrue(success)


	def test_without_token_is_authenticated(self):
		
		with patch("app.src.common.decorators.request") as mock_request:
			with patch("app.src.common.decorators.Utils", new_callable=MockUtils):
				mock_request.headers = dict()
				responseWithoutHeader = is_authenticated(self.func)()

				mock_request.headers = dict(Authorization="")
				responseWithoutToken = is_authenticated(self.func)()

		self.assertDictEqual(responseWithoutHeader, 
			dict(status=401, data="Token must be a bearer token", message= "Invalid token"))

		self.assertDictEqual(responseWithoutToken, 
			dict(status=401, data="Token must be a bearer token", message= "Invalid token"))


	def test_without_session_is_authenticated(self):

		with patch("app.src.common.decorators.request") as mock_request:

			mock_request.headers = dict(Authorization=self.bearer_token)
			with patch("app.src.common.decorators.Utils", new_callable=MockUtils):

				with patch("app.src.common.decorators.Auth.token_decode", return_value=dict(token="session token")):

					with patch("app.src.common.decorators.Auth.session_exists", return_value=False):

						response = is_authenticated(self.func)()

		self.assertDictEqual(response, 
			dict(message="Invalid token", status=401, data= "User does not have an active session"))
						

	def test_success_refresh_token(self):

		with patch("app.src.common.decorators.request") as mock_request:

			mock_request.headers = dict(REFRESH_TOKEN=self.bearer_token)
			with patch("app.src.common.decorators.Auth.refresh_token_exists", return_value=True):

				success = refresh_token("TEST")(self.func)()
						
		self.assertTrue(success)

	def test_without_token_refresh_token(self):

		with patch("app.src.common.decorators.request") as mock_request:

			with patch("app.src.common.decorators.Utils", new_callable=MockUtils):
				
				mock_request.headers = dict()
				responseWithoutHeader = refresh_token("TEST")(self.func)()

				mock_request.headers = dict(REFRESH_TOKEN="")
				responseWithoutToken = refresh_token("TEST")(self.func)()
						
		self.assertDictEqual(responseWithoutHeader, dict(message="Invalid token", data="Token must be a bearer token", status=401))
		self.assertDictEqual(responseWithoutToken, dict(message="Invalid token", data="Token must be a bearer token", status=401))

	def test_without_refresh_token_refresh_token(self):
		
		with patch("app.src.common.decorators.request") as mock_request:

			mock_request.headers = dict(REFRESH_TOKEN=self.bearer_token)
			with patch("app.src.common.decorators.Utils", new_callable=MockUtils):

					with patch("app.src.common.decorators.Auth.refresh_token_exists", return_value=False):

						response = refresh_token("TEST")(self.func)()

		self.assertDictEqual(response, 
			dict(message="Invalid token", status=401, data="Invalid refresh token"))