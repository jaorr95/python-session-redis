from sqlalchemy_utils import EmailType
from app.config.config import db
from app.src.common.utils import Utils


class Admin(db.Model):

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	username = db.Column(db.String(50), nullable=False, unique=True)
	_salt = db.Column(db.String(255), nullable=False)
	_password = db.Column(db.String(255), nullable=False)

	def __str__(self):

		return "Admin: <id={1}, username={0}, password={2}, salt={3}>".format(self.username,
			 self.id, self._password, self._salt)

	def __repr__(self):

		return "Admin: <id={1}, username={0}, password={2}, salt={3}>".format(self.username,
			 self.id, self._password, self._salt)

	@property
	def password(self):

		return (self._salt, self._password)

	@password.setter
	def password(self, plain_password):

		self._salt, self._password = Utils.hash_password(plain_password) 