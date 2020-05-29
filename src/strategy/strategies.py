from abc import  ABC, abstractmethod

class SignupStrategy(ABC):

	@abstractmethod
	def signup(self):
		pass


class LoginStrategy(ABC):

	@abstractmethod
	def login(self) -> dict:
		pass

class RefreshTokenStrategy(ABC):

	@abstractmethod
	def refresh(self) -> dict:
		pass