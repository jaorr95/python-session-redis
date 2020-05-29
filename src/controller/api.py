import json
from flask import request
from flask_restful import Resource

import sys
sys.path.append("../../..")

from app.config.config import api, app, config
from app.src.bo.manage_users import ManageUser
from app.src.strategy.signup_user_strategy import SignupUserStrategy
from app.src.strategy.signup_admin_strategy import SignupAdminStrategy
from app.src.strategy.login_admin_strategy import LoginAdminStrategy
from app.src.strategy.login_user_strategy import LoginUserStrategy
from app.src.strategy.refresh_token_admin_strategy import RefreshTokenAdminStrategy
from app.src.strategy.refresh_token_user_strategy import RefreshTokenUserStrategy
from app.src.common.utils import Utils
from app.src.common.auth import Auth
from app.src.common.decorators import is_authenticated, refresh_token
from app.src.schemas.admin_schemas import AdminCreateSchema
from app.src.schemas.user_schemas import UserCreateSchema
from app.src.exceptions.errors import InvalidParametersError, UserExistsError, AuthenticationError, InvalidTokenError

config.init_db()

class HelloAdmin(Resource):

	@is_authenticated
	def get(self):
		return dict(result=200, message="admin logged")

api.add_resource(HelloAdmin, "/admin/secure/profile")


class HelloUser(Resource):

	@is_authenticated
	def get(self):	
		return dict(result=200, message="user logged")

api.add_resource(HelloUser, "/user/secure/profile")


class RegisterUser(Resource):

	def post(self):

		manage = ManageUser()
		strategy = SignupUserStrategy()
		try:

			user = manage.signup(strategy, request.json)
			data = UserCreateSchema().dumps(user)
		except InvalidParametersError as e:
			return Utils.response(status=e.status, data=e.errors, message="Invalid parameters")

		except UserExistsError as e:
			return Utils.response(status=e.status, data=e.errors, message="Parameter must be unique")

		return Utils.response(status=201, data=json.loads(data), message="Request succesfull")

api.add_resource(RegisterUser, "/user/sign-up")


class RegisterAdmin(Resource):

	def post(self):

		manage = ManageUser()
		strategy = SignupAdminStrategy()
		try:
			admin = manage.signup(strategy, request.json)
			data = AdminCreateSchema().dumps(admin)
			
		except InvalidParametersError as e:
			return Utils.response(status=e.status, data=e.errors, message="Invalid parameters")

		except UserExistsError as e:
			return Utils.response(status=e.status, data=e.errors, message="Parameter must be unique")
		
		return Utils.response(status=201, data=json.loads(data), message="Request succesfull")

api.add_resource(RegisterAdmin, "/admin/sign-up")


class LoginUser(Resource):

	def post(self):

		manage = ManageUser()
		strategy = LoginUserStrategy()
		try:
			tokens = manage.login(strategy, request.json)

		except InvalidParametersError as e:
			return Utils.response(status=e.status, data=e.errors, message="Invalid parameters")
		
		except AuthenticationError as e:
			return Utils.response(status=e.status, data=e.errors, message="Invalid credentials")

		return Utils.response_auth(tokens["token_id"], tokens["refresh_token"])
		
api.add_resource(LoginUser, "/user/login")


class LoginAdmin(Resource):

	def post(self):

		manage = ManageUser()
		strategy = LoginAdminStrategy()

		try:
			tokens = manage.login(strategy, request.json)

		except InvalidParametersError as e:
			return Utils.response(status=e.status, data=e.errors, message="Invalid parameters")
		
		except AuthenticationError as e:
			return Utils.response(status=e.status, data=e.errors, message="Invalid credentials")

		return Utils.response_auth(tokens["token_id"], tokens["refresh_token"])
		
api.add_resource(LoginAdmin, "/admin/login")


class LogoutUser(Resource):

	@is_authenticated
	def get(self):

		token = request.headers.get("Authorization").split(" ")[-1]
		Auth.delete_session(token)

		return Utils.response(message="Request succesfull")
		
api.add_resource(LogoutUser, "/user/secure/logout")


class LogoutAdmin(Resource):

	@is_authenticated
	def get(self):

		token = request.headers.get("Authorization").split(" ")[-1]
		Auth.delete_session(token)

		return Utils.response(message="Request succesfull")
		
api.add_resource(LogoutAdmin, "/admin/secure/logout")


class RefreshUser(Resource):

	@refresh_token("USER")
	def get(self):

		refresh_token = request.headers.get("REFRESH_TOKEN").split(" ")[-1]
		maneger = ManageUser()
		strategy = RefreshTokenUserStrategy()
		tokens = maneger.refresh(strategy, refresh_token)

		return Utils.response_auth(tokens["token_id"], tokens["refresh_token"])
		
api.add_resource(RefreshUser, "/user/refresh")


class RefreshAdmin(Resource):

	@refresh_token("ADMIN")
	def get(self):

		refresh_token = request.headers.get("REFRESH_TOKEN").split(" ")[-1]
		maneger = ManageUser()
		strategy = RefreshTokenAdminStrategy()
		tokens = maneger.refresh(strategy, refresh_token)

		return Utils.response_auth(tokens["token_id"], tokens["refresh_token"])
		
api.add_resource(RefreshAdmin, "/admin/refresh")

if __name__ == "__main__":
	app.run(debug=True)