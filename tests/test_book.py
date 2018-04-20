import unittest
from run import app
import json
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)


class TestFlaskApi(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_home_status_code(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_home_data(self):
        response = self.app.get('/')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data["message"], "it works")

    def test_register_user_status_code(self):
        #  invalid url
        response = self.app.post('/api/v1/auth')
        self.assertEqual(response.status_code, 404)

        # valid url
        response = self.app.post('/api/v1/auth/register')
        self.assertEqual(response.status_code, 200)

        # request method bad
        response = self.app.get('/api/v1/auth/register')
        self.assertEqual(response.status_code, 405)

    def test_register_user_data(self):
        user = {}
        response = self.app.post('/api/v1/auth/register', data=json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_login_status_code(self):
        response = self.app.post('/api/v1/auth/login')
        self.assertEqual(response.status_code, 200)

    def test_get_all_book(self):
        response = self.app.get('/api/v1/books')
        self.assertEqual(response.status_code, 200)

    def test_a_book(self):
        response = self.app.get('/api/v1/books/1')
        self.assertEqual(response.status_code, 200)

    def test_borrow_a_book(self):
        user = {"username": "mike", "password": 123456789}
        access_token = create_access_token(identity=user["username"])
        print(access_token)
        response = self.app.get('/api/v1/users/books/1')
        self.assertEqual(response.status_code, 200)

    def test_modify_a_book(self):
        response = self.app.put('/api/v1/books/1')
        self.assertEqual(response.status_code, 200)

    def test_delete_book(self):
        response = self.app.delete('/api/v1/books/1')
        self.assertEqual(response.status_code, 200)

    def test_post_book(self):
        response = self.app.post('/api/v1/books')
        self.assertEqual(response.status_code, 200)

    def test_reset_password(self):
        response = self.app.post('/api/auth/reset-password')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
