from unittest import TestCase
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
import jwt
from app.src.common.auth import Auth, SESSION_KEY, REFRESH_TOKEN_KEY
from app.src.exceptions.errors import InvalidTokenError

class TestSessionsToken(TestCase):

	def setUp(self):
		self.secret_key = "secret_key"
		self.algorithms = ["HS256"]
		self.data = dict(id=1, name="test")
		self.role = "test"

	def tearDown(self):
		self.secret_key = None
		self.algorithms = None
		self.data = None
		self.role = None

	def test_encode_jwt(self):

		token = Auth.token_encode(self.data)
		self.assertIsNotNone(token)
		token_decode = jwt.decode(token, self.secret_key, algorithms=self.algorithms)
		self.assertEqual(self.data, token_decode)		

	def test_decode_jwt(self):
		
		token = jwt.encode(self.data, key=self.secret_key, algorithm=self.algorithms[0])
		token_decode = Auth.token_decode(token)
		self.assertIsNotNone(token_decode)
		self.assertEqual(self.data, token_decode)

	def test_decode_jwt_fail(self):

		with self.assertRaises(InvalidTokenError):
			Auth.token_decode(None)

		with self.assertRaises(InvalidTokenError):
			self.data["exp"] = datetime.now() - timedelta(seconds=30)
			token = jwt.encode(self.data, key=self.secret_key, algorithm=self.algorithms[0])
			Auth.token_decode(token)

	def test_generate_session_token(self):

		with patch("app.src.common.auth.Auth.session_token", return_value="session token"):
			with patch("app.src.common.auth.Auth.token_encode", return_value="token jwt"):
				with patch("app.src.common.auth.Auth.refresh_token", return_value="refresh token"):
					with patch("app.src.common.auth.Auth.save_session", return_value=None):
						tokens = Auth.generate_session_token(self.role, **self.data)

		self.assertIsNotNone(tokens)
		self.assertDictEqual(dict(token_id="token jwt", refresh_token="refresh token"), tokens)
	

	def test_get_session_token(self):

		token = Auth.session_token()
		self.assertIsNotNone(token)

	def test_get_refresh_token(self):

		token = Auth.refresh_token()
		self.assertIsNotNone(token)


class MockRedis:
	pass

"""	def __init__(self, role, session):
		self.role = role
		self.session = session

	def hget(self, *args, **kwargs):
		return self.role

	def hgetall(self, *args, **kwargs):
		return self.session

	def delete(self, *args, **kwargs):
		pass
"""


class TestSessionRedis(TestCase):

	def setUp(self):
		self.role = "test"
		self.session = dict(refresh_id="refresh")
		self.mock_redis = MockRedis()
		self.mock_redis.hget = MagicMock(return_value=self.role)
		self.mock_redis.hgetall = MagicMock(return_value=self.session)
		self.mock_redis.delete = MagicMock(return_value=None)
		self.mock_redis.hmset = MagicMock(return_value=None)
		self.mock_redis.expireat = MagicMock(return_value=None)
		self.jwt_decode = dict(token="token")
		self.session_id = SESSION_KEY+"session"
		self.refresh_id = REFRESH_TOKEN_KEY+"session"

	def tearDown(self):
		self.role = None
		self.session = None
		self.mock_redis = None
		self.jwt_decode = None
		self.session_id = None
		self.refresh_id = None

	def test_session_exists(self):

		with patch("app.src.common.auth.config.redis", new=self.mock_redis) as mock_redis:
			exists =Auth.session_exists("session_id", self.role)
		
		self.assertTrue(exists)

	def test_session_not_exists(self):

		with patch("app.src.common.auth.config.redis", new=self.mock_redis) as mock_redis:
			exists =Auth.session_exists("session_id", "not")
		
		self.assertFalse(exists)

	def test_refresh_token_exists(self):

		with patch("app.src.common.auth.config.redis", new=self.mock_redis) as mock_redis:
			exists =Auth.refresh_token_exists("refresh_id", self.role)
		
		self.assertTrue(exists)

	def test_refresh_token_not_exists(self):

		with patch("app.src.common.auth.config.redis", new=self.mock_redis) as mock_redis:
			exists =Auth.refresh_token_exists("refresh_id", "not")
		
		self.assertFalse(exists)

	def test_get_session(self):

		with patch("app.src.common.auth.config.redis", new=self.mock_redis):
			session = Auth.get_session("refresh_id")
		
		self.assertDictEqual(session, self.session)

	def test_delete_session(self):

		with patch("app.src.common.auth.Auth.token_decode", return_value=self.jwt_decode):
			with patch("app.src.common.auth.config.redis", new=self.mock_redis) as mock:
				Auth.delete_session("token_jwt")
				mock.hgetall.assert_called_with(SESSION_KEY+self.jwt_decode["token"])
				mock.delete.assert_any_call(SESSION_KEY+self.jwt_decode["token"])
				mock.delete.assert_any_call(self.session["refresh_id"])

	def test_update_session(self):

		with patch("app.src.common.auth.Auth.generate_session_token", return_value=dict()):
			with patch("app.src.common.auth.config.redis", new=self.mock_redis) as mock:
				data = dict(name="test", id=1)
				refresh = "refresh_token"
				new_session = Auth.update_session(refresh, **data)

				mock.hget.assert_any_call(REFRESH_TOKEN_KEY+refresh, "session")
				mock.hget.assert_any_call(self.role, "ROLE")
				mock.delete.assert_any_call(REFRESH_TOKEN_KEY+refresh)
				mock.delete.assert_any_call(self.role)

		self.assertDictEqual(new_session, dict())

	def test_save_session(self):

		with patch("app.src.common.auth.config.redis", new=self.mock_redis) as mock:
			data = dict(name="test", id=1, ROLE="test")
			Auth.save_session(self.session_id.split(":")[1], self.refresh_id.split(":")[1], **data)
			data["refresh_id"] = self.refresh_id
			mock.hmset.assert_any_call(self.session_id, data)
			mock.hmset.assert_any_call(self.refresh_id, dict(ROLE=data["ROLE"], session=self.session_id))
