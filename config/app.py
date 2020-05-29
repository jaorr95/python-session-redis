from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from redis import Redis
from app.src.common.utils import Singleton

class App(object, metaclass=Singleton):


	def __init__(self):

		self.app = Flask(__name__, instance_relative_config=True)
		self.app.config.from_mapping(
			SECRET_KEY="dev"
			)
		self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/test.db"

		self.api = Api(self.app)
		self.db = SQLAlchemy(self.app)
		self.ma = Marshmallow(self.app)
		self.redis = Redis(host="127.0.0.1", port=6379, db=0, decode_responses=True)

	
	def init_db(self):
		
		import app.src.models
		self.db.create_all()

