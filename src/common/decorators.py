from functools import wraps
from flask import request
from app.src.common.utils import Auth, Utils
from app.src.exceptions.errors import InvalidTokenError


def is_authenticated(f):

	@wraps(f)
	def wrapper(*args, **kwars):

		token = request.headers.get("Authorization")
		role = Utils.request_role()

		try:
			if not token or token.split(" ")[0] != "Bearer":
				raise InvalidTokenError(token, "Token must be a bearer token", "Invalid token")
			
			token_decode = Auth.token_decode(token.split(" ")[1])
			session_id = token_decode["token"]
			exists = Auth.session_exists(session_id, role)

			if not exists:
				raise InvalidTokenError(token, "User does not have an active session", "Invalid token")


		except InvalidTokenError as e:
			return Utils.response(status=e.status, message="Invalid token", data=e.errors)

		return f(*args, **kwars)

	return wrapper


def refresh_token(role: str):

	def decorator(f):

		@wraps(f)
		def wrapper(*args, **kwars):

			token = request.headers.get("REFRESH_TOKEN")

			try:
				if not token or token.split(" ")[0] != "Bearer":
					raise InvalidTokenError(None, token, "Token must be a bearer token", "Invalid token")
				
				exists = Auth.refresh_token_exists(token.split(" ")[1], role)

				if not exists:
					raise InvalidTokenError(None, token, "Invalid refresh token", "Invalid token")


			except InvalidTokenError as e:
				return Utils.response(status=e.status, message="Invalid token", data=e.errors)

			return f(*args, **kwars)

		return wrapper

	return decorator