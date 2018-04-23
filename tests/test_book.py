import unittest
from run import app
from app import models
import json


class TestFlaskApi(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.book = models.Books()

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
        response = self.app.post('/api/v1/auth/register',
                                 data=json.dumps(user),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_login_status_code(self):
        user = {"username": "chris.mutua", "password": "789456123]"}
        response = self.app.post('/api/v1/auth/login',
                                 data=json.dumps(user),
                                 content_type='application/json')
        self.assertEqual(user["username"], "chris.mutua")

    def test_get_all_book(self):
        response = self.app.get('/api/v1/books')
        self.assertEqual(response.status_code, 200)

    def test_get_a_book(self):
        response = self.app.get('/api/v1/books/1')
        self.assertEqual(response.status_code, 200)

    # def test_borrow_a_book(self):
    #     jwt = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9" \
    #           ".eyJpYXQiOjE1MjQyMDY4NzQsIm5iZiI6MTUyNDIwNjg3NCwi" \
    #           "anRpIjoiYjdkNDkxOTYtMjA1MC00YWI3LTkxZjMtZDM4N2Y4YzYzNWU5" \
    #           "IiwiZXhwIjoxNTI0MjA3Nzc0LCJpZGVudGl0eSI6InJlZ2luYS5udGhpd2EiLCJmcmVzaCI6ZmFsc2UsInR5cGUiOiJhY2Nlc3" \
    #           "MifQ.035xsRCwq4svkBJkr_CRMpMWroIV1auezpimhnYWryo"
    #     response = self.app.get('/api/v1/users/books/1',
    #                             content_type='application/json',
    #                             headers=dict(Authorization="Bearer " + jwt))
    #
    #     self.assertEqual(response.status_code, 200)

    def test_modify_a_book(self):
        book = {"title": "Harry"}
        response = self.app.put('/api/v1/books/1', data=json.dumps(book), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_modify_book_title_method(self):
        response = self.book.modify_book_title(1, "harry")
        self.assertEqual(response, [{"Author": "J.K.Rowling", "Copies": 3, "Title": "harry"}])

    def test_delete_book(self):
        response = self.app.delete('/api/v1/books/1')
        self.assertEqual(response.status_code, 400)

    def test_post_book(self):
        book = {"book_id": 1, "title": "River Between", "author": "Chinua Achebe"}
        response = self.app.post('/api/v1/books',
                                 data=json.dumps(book),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_reset_password(self):
        user = {"username": 'mike.nthiwa', "password": "Mutuamike$#@!"}
        response = self.app.post('/api/auth/reset-password',
                                 data=json.dumps(user),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_book_id(self):

        result = self.book.get_a_book(book_id)
        self.assertEqual(result, [{'Title': 'Harry Potter', 'Author': 'J.K.Rowling', 'Copies': 3}])


if __name__ == '__main__':
    unittest.main()
