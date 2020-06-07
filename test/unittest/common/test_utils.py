from unittest import TestCase
from unittest.mock import patch
from app.src.common.utils import Utils


class TestCheckPasswords(TestCase):

	def setUp(self):
		self.password = "123456"

	def tearDown(self):
		self.password = None

	def test_hash_password_is_not_none(self):
		
		salt, password = Utils.hash_password(self.password)
		self.assertIsNotNone(salt)
		self.assertIsNotNone(password)

	def test_check_valid_hash_and_plain_password(self):
		s_salt, s_password = Utils.hash_password(self.password)
		isCheck = Utils.verify_password(s_salt, s_password, self.password)
		self.assertTrue(isCheck)

	def test_check_hash_and_invalid_plain_password(self):
		invalid_password = "abcd"
		s_salt, s_password = Utils.hash_password(self.password)
		isCheck = Utils.verify_password(s_salt, s_password, invalid_password)
		self.assertFalse(isCheck)


class TestCheckRoles(TestCase):

	def setUp(self):
		self.roles = ["ADMIN", "USER"]
		
	def tearDown(self):
		self.roles = None

	def test_check_role_admin(self):

		with patch("app.src.common.utils.request") as mock_request:

			mock_request.path = "/admin/secure/*"
			role = Utils.request_role()
		
		self.assertIn(role, self.roles)
		self.assertEqual(role, self.roles[0])

	def test_check_role_user(self):

		with patch("app.src.common.utils.request") as mock_request:

			mock_request.path = "/user/secure/*"
			role = Utils.request_role()
		
		self.assertIn(role, self.roles)
		self.assertEqual(role, self.roles[1])

	def test_check_fail_role(self):

		with patch('app.src.common.utils.request') as mock_request:

			mock_request.path = "/hola/*"
			role = Utils.request_role()
		
		self.assertNotIn(role, self.roles)
		self.assertIsNone(role)





