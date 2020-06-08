from app.src.strategy.strategies import SignupStrategy, LoginStrategy, RefreshTokenStrategy


class MockSignupUserStrategy(SignupStrategy):

	def signup():
		pass

class MockSignupAdminStrategy(SignupStrategy):

	def signup():
		pass
	

class MockLoginAdminStrategy(LoginStrategy):

	def login():
		pass
	

class MockLoginUserStrategy(LoginStrategy):
	
	def login():
		pass

class MockRefreshTokenAdminStrategy(RefreshTokenStrategy):

	def refresh():
		pass

class MockRefreshTokenUserStrategy(RefreshTokenStrategy):

	def refresh():
		pass


	
