import re
import bcrypt
import hashlib
import binascii
from flask import jsonify, request


class Singleton(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):

        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)

        return cls._instances[cls]


class Utils(object):

	@staticmethod
	def hash_password(password: str, iterations=100000) -> tuple:

		salt = bcrypt.gensalt()
		hash_pass = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, iterations)
		hash_pass = binascii.hexlify(hash_pass)

		return (salt.decode(), hash_pass.decode())

	@staticmethod
	def verify_password(stored_salt: str, stored_hash_pass: str, password: str, iterations=100000) -> bool:
		
		hash_pass = hashlib.pbkdf2_hmac("sha256", password.encode(), stored_salt.encode(), iterations)
		hash_pass = binascii.hexlify(hash_pass).decode()

		return stored_hash_pass == hash_pass

	@staticmethod
	def response_auth(token_id: str, refresh_token: str, status=200):
		response =  dict(status=status, token_id=token_id, refresh_token=refresh_token)
		return jsonify(response)

	@staticmethod
	def response(*, status=200, data=[], message=""):
		return jsonify(status=status, data=data, message=message)

	@staticmethod
	def request_role() -> str:

		from app.config.config import ROLES
		role = None

		for route, r in ROLES.items():
			if re.match(route, request.path):
				role = r
				break

		return role