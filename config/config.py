from app.config.app import App

config = App()
db = config.db
ma = config.ma
api = config.api
app = config.app
redis = config.redis

ROLES = {
	"/admin/secure/*": "ADMIN",
	"/user/secure/*": "USER"
}