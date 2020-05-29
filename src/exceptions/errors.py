class Error(Exception):
	
	def __init__(self, data, message, previous=None):

		self.data = data
		self.message = message
		self.previous = previous


class InvalidParametersError(Error):

	def __init__(self, data, errors, message, previous=None, status=400):

		super().__init__(data, message, previous)
		self.status = status
		self.errors = errors


class UserExistsError(Error):

	def __init__(self, data, errors, message, previous=None, status=412):

		super().__init__(data, message, previous)
		self.status = status
		self.errors = errors


class AuthenticationError(Error):

	def __init__(self, data, errors, message, previous=None, status=401):

		super().__init__(data, message, previous)
		self.status = status
		self.errors = errors


class InvalidTokenError(Error):

	def __init__(self, data, errors, message, previous=None, status=401):

		super().__init__(data, message, previous)
		self.status = status
		self.errors = errors