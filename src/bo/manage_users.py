from app.src.strategy.strategies import SignupStrategy, LoginStrategy, RefreshTokenStrategy
from app.src.exceptions.errors import AuthenticationError


class ManageUser(object):

	def signup(self, signupStrategy: SignupStrategy, data):	
		
		register = signupStrategy.signup(data)
		
		return register

	def login(self, loginStrategy: LoginStrategy, credentials) -> dict:	
		
		tokens = loginStrategy.login(credentials)

		if tokens is None:
			raise AuthenticationError(
				credentials, "Invalid credentials",
				"Error occurred when trying to login")

		return tokens

	def refresh(self, refreshTokenStrategy: RefreshTokenStrategy, refresh_token) -> dict:

		tokens = refreshTokenStrategy.refresh(refresh_token)

		return tokens