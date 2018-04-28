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
        #  Test if no value is provided
        response = self.app.post('/api/v1/auth/register',
                                 data=json.dumps(user),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)

        # Test if only email is provided
        user1 = {"username": None, "password": None, "email": "mike.nthiwa@gmail.com"}
        response1 = self.app.post('/api/v1/auth/register',
                                  data=json.dumps(user1),
                                  content_type='application/json')
        self.assertEqual(response1.status_code, 200)

        #  Test if only password is provided
        user2 = {"username": None, "email": None, "password": "Michael$#@!"}
        response2 = self.app.post('/api/v1/auth/register',
                                  data=json.dumps(user2),
                                  content_type='application/json')
        self.assertEqual(response2.status_code, 200)

        #  Test if only username is provided
        user3 = {"username": "mike.nthiwa", "email": None, "password": None}
        response3 = self.app.post('/api/v1/auth/register',
                                  data=json.dumps(user3),
                                  content_type='application/json')
        self.assertEqual(response3.status_code, 200)

        #  Test when username is missing
        user4 = {"username": None, "email": "mike.nthiwa@gmail.com", "password": "Michael$#@!"}
        response4 = self.app.post('/api/v1/auth/register',
                                  data=json.dumps(user4),
                                  content_type='application/json')
        self.assertEqual(response4.status_code, 200)

        #  Test when email is missing
        user5 = {"username": "mike.nthiwa", "email": None, "password": "Michael$#@!"}
        response5 = self.app.post('/api/v1/auth/register',
                                  data=json.dumps(user5),
                                  content_type='application/json')
        self.assertEqual(response5.status_code, 200)

        #  Test when password is missing
        user6 = {"username": "mike.nthiwa", "email": "mike.nthiwa@gmail.com", "password": None}
        response6 = self.app.post('/api/v1/auth/register',
                                  data=json.dumps(user6),
                                  content_type='application/json')
        self.assertEqual(response6.status_code, 200)

        #  Test if password does not meet requirement
        user7 = {"username": "mike.nthiwa", "email": "mike.nthiwa@gmail.com", "password": "mic"}
        response7 = self.app.post('/api/v1/auth/register',
                                  data=json.dumps(user7),
                                  content_type='application/json')
        self.assertEqual(response7.status_code, 200)

        #  Test if all fields a filled correctly
        user7 = {"username": "mike.nthiwa", "email": "mike.nthiwa@gmail.com", "password": "Michael%$#@!"}
        response7 = self.app.post('/api/v1/auth/register',
                                  data=json.dumps(user7),
                                  content_type='application/json')
        self.assertEqual(response7.status_code, 200)

    def test_login_status_code(self):

        # Test when request is not json
        user = {"username": None, "password": None}
        response = self.app.post('/api/v1/auth/login',
                                 data=json.dumps(user),
                                 content_type='')
        self.assertEqual(response.status_code, 400)

        # Test if all fields are empty
        user = {"username": None, "password": None}
        response = self.app.post('/api/v1/auth/login',
                                 data=json.dumps(user),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)

        # Test when only password is provided
        user1 = {"username": None, "password": "Michael$%#@!"}
        response1 = self.app.post('/api/v1/auth/login',
                                  data=json.dumps(user1),
                                  content_type='application/json')
        self.assertEqual(response1.status_code, 200)

        # Test when only username is provided
        user3 = {"username": "mike.nthiwa", "password": None}
        response3 = self.app.post('/api/v1/auth/login',
                                  data=json.dumps(user3),
                                  content_type='application/json')
        self.assertEqual(response3.status_code, 200)

        # Test if username is in db
        user = {"username": "mike", "password": "Michael$$#@!"}
        response = self.app.post('/api/v1/auth/login',
                                 data=json.dumps(user),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)

        # Test if password matches to the username
        user = {"username": "mike.nthiwa", "password": "Michae"}
        response = self.app.post('/api/v1/auth/login',
                                 data=json.dumps(user),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)

        #  Test when all field are filled correctly
        user2 = {"username": "mike.nthiwa", "password": "Michael$$#@!"}
        response2 = self.app.post('/api/v1/auth/login',
                                  data=json.dumps(user2),
                                  content_type='application/json')
        self.assertEqual(response2.status_code, 200)

    def test_get_all_book(self):
        response = self.app.get('/api/v1/books')
        self.assertEqual(response.status_code, 200)

    def test_get_a_book(self):
        response = self.app.get('/api/v1/books/1')
        self.assertEqual(response.status_code, 200)

        response1 = self.app.put('/api/v1/books/1',
                                 content_type='')
        self.assertEqual(response1.status_code, 400)

    # def test_borrow_a_book(self):
    #     jwt = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1MjQ4MDY5OTcsIm5iZiI6MTUyN" \
    #           "DgwNjk5NywianRpIjoiYTBjMzVkMDMtZGQ3NC00NTEyLWJkOTEtZDQwOGQwMzAyMTI2IiwiZXhwIj" \
    #           "oxNTI0ODA3ODk3LCJpZGVudGl0eSI6InJlZ2luYS5udGhpd2EiLCJmcmVzaCI6ZmFsc2UsInR5cGUiOi" \
    #           "JhY2Nlc3MifQ.X-RNJc1O69yev7Fd2J7BnnIk4LEf-00cY-bPY2d-yWQ"
    #     response = self.app.get('/api/v1/users/books/1',
    #                             content_type='application/json',
    #                             headers=dict(Authorization="Bearer " + jwt))
    #
    #     self.assertEqual(response.status_code, 200)
    #
    #     book_id = 1
    #     all_books = self.book.get_all_books()
    #     self.assertIn(book_id, all_books.keys())

    def test_modify_a_book(self):
        book = {"title": "Harry"}
        response = self.app.put('/api/v1/books/1', data=json.dumps(book), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_delete_book(self):
        response = self.app.delete('/api/v1/books/1')
        self.assertEqual(response.status_code, 400)

    def test_post_book(self):
        book = {"book_id": 3, "title": "The Storm", "author": "Blake Banner", "copies": 3}
        response = self.app.post('/api/v1/books',
                                 data=json.dumps(book),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)

        book1 = {"book_id": 3, "title": "The Storm", "author": "Blake Banner", "copies": 3}
        response1 = self.app.post('/api/v1/books',
                                  data=json.dumps(book1),
                                  content_type='')
        self.assertEqual(response1.status_code, 400)

    def test_reset_password(self):
        user = {"username": 'mike.nthiwa', "password": "Mutuamike$#@!"}
        response = self.app.post('/api/auth/reset-password',
                                 data=json.dumps(user),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)

        # Test if request is not json
        user1 = {"username": 'mike.nthiwa', "password": "Mutuamike$#@!"}
        response1 = self.app.post('/api/auth/reset-password',
                                  data=json.dumps(user1),
                                  content_type='')
        self.assertEqual(response1.status_code, 400)


if __name__ == '__main__':
    unittest.main()
