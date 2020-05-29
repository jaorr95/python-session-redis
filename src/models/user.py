from sqlalchemy_utils import EmailType
from app.config.config import db
from app.src.common.utils import Utils


class User(db.Model):

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(50), nullable=False)
	lastname = db.Column(db.String(50), nullable=False)
	email = db.Column(EmailType, nullable=False, unique=True)
	user_type = db.Column(db.Integer, nullable=False, default=2)
	_salt = db.Column(db.String(255), nullable=False)
	_password = db.Column(db.String(255), nullable=False)

	def __str__(self):

		return "User: <id={2}, name={0}, lastname={1}, email={3}>".format(self.name,
			self.lastname, self.id, self.email)

	def __repr__(self):

		return "User: <id={2}, name={0}, lastname={1}, email={3}>".format(self.name,
			self.lastname, self.id, self.email)

	@property
	def password(self):

		return (self._salt, self._password)

	@password.setter
	def password(self, plain_password):

		self._salt, self._password = Utils.hash_password(plain_password) 