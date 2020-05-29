from datetime import datetime, timedelta
import bcrypt
import hashlib
import jwt
from app.src.exceptions.errors import InvalidTokenError
from app.config import config

REFRESH_TOKEN_KEY = "refresh:"
SESSION_KEY = "sess:"
JWT_EXPIRE = 300 # in seconds
REFRESH_TIME = 24 # in hours


class Auth(object):

	@staticmethod
	def generate_session_token(role: str, **data) -> dict:
		
		data["exp"] = datetime.utcnow() + timedelta(seconds=JWT_EXPIRE)
		data["iat"] = datetime.utcnow()
		data["token"] = Auth.session_token()
		data["ROLE"] = role
		token_jwt = Auth.token_encode(data)
		token = data.pop("token")
		refresh_token = Auth.refresh_token()
		Auth.save_session(token, refresh_token, **data)

		return dict(token_id=token_jwt, refresh_token=refresh_token)

	@staticmethod
	def session_token() -> str:

		return hashlib.md5(bcrypt.gensalt()).hexdigest()

	@staticmethod
	def refresh_token() -> str:

		return hashlib.sha256(bcrypt.gensalt()).hexdigest()

	@staticmethod	
	def token_encode(data: dict) -> str:

		jwt_encoded = jwt.encode(data, "secret_key", algorithm="HS256")

		return jwt_encoded.decode()

	@staticmethod
	def token_decode(token_jwt: str) -> str:

		try:

			token_decoded = jwt.decode(token_jwt, "secret_key", algorithms=["HS256"], options={"require": ["exp", "iat"]})
			
		except jwt.exceptions.PyJWTError as e:

			raise InvalidTokenError(token_jwt, e.args, "Error ocurrs trying to decode token jwt", e)

		return token_decoded

	@staticmethod
	def save_session(session_id: str, refresh_token: str, **data) -> None:

		session_id = SESSION_KEY+session_id
		refresh_id = REFRESH_TOKEN_KEY+refresh_token
		data["refresh_id"] = refresh_id
		config.redis.hmset(session_id, data)
		config.redis.hmset(refresh_id, dict(ROLE=data["ROLE"], session=session_id))
		config.redis.expireat(session_id, datetime.now() + timedelta(hours=REFRESH_TIME))
		config.redis.expireat(refresh_id, datetime.now() + timedelta(hours=REFRESH_TIME))

	@staticmethod
	def session_exists(session_id: str, role: str) -> bool:

		session = config.redis.hget(SESSION_KEY+session_id, "ROLE")

		return session == role

	@staticmethod
	def refresh_token_exists(refresh_token: str, role: str) -> bool:
		
		refresh = config.redis.hget(REFRESH_TOKEN_KEY+refresh_token, "ROLE")

		return refresh == role

	@staticmethod
	def delete_session(token_jwt: str) -> None:

		token_decoded = Auth.token_decode(token_jwt)
		session = config.redis.hgetall(SESSION_KEY+token_decoded["token"])
		refresh_id = session["refresh_id"]
		config.redis.delete(SESSION_KEY+token_decoded["token"])
		config.redis.delete(refresh_id)

	@staticmethod
	def get_session(refresh_token: str) -> dict:

		session_id = config.redis.hget(REFRESH_TOKEN_KEY+refresh_token, "session")

		return config.redis.hgetall(session_id)

	@staticmethod
	def update_session(refresh_token: str, **data) -> dict:
		
		session_id = config.redis.hget(REFRESH_TOKEN_KEY+refresh_token, "session")
		role = config.redis.hget(session_id, "ROLE")
		new_session = Auth.generate_session_token(role, **data)
		config.redis.delete(REFRESH_TOKEN_KEY+refresh_token)
		config.redis.delete(session_id)

		return new_session