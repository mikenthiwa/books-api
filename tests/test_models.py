import unittest
from app import models


class TestModels(unittest.TestCase):
    def setUp(self):
        self.book = models.Books()
        self.user = models.Users()

    # Testing books model
    def test_modify_book_title_method(self):
        """Testing the modify title method if it modifies title of book"""
        book_id = 1
        title = "Harry Potter and Chamber of secrets"
        response = self.book.modify_book_title(book_id, title)
        self.assertEqual(response, [{"Author": "J.K.Rowling", "Copies": 3, "Title": title}])

    def test_modify_book_author_method(self):
        """Testing the modify author method if it modifies author of book """
        book_id = 3
        author = "Chinua Achebe"
        response = self.book.modify_book_author(book_id, author)
        self.assertEqual(response, [{"Title": "The Storm", "Author": "Chinua Achebe", "Copies": 3}])

    def test_modify_book_copies_method(self):
        """Testing the modify copies method if it modifies copies of book"""
        book_id = 3
        copies = 4
        response = self.book.modify_book_copies(book_id, copies)
        self.assertEqual(response, [{"Title": "The Storm", "Author": "Chinua Achebe", "Copies": copies}])

    def test_delete_book_method(self):
        """Testing the delete method deletes book"""
        result = self.book.delete_book(2)
        self.assertNotIn(self.book.get_a_book(2), result)

    def test_borrow_book_method(self):
        """Testing borrow book method"""
        book_id = 2
        response = self.book.borrow_book(book_id)
        self.assertEqual(response, [{"Title": "The whistler", "Author": "John Grisham", "Copies": 3}])

    # Testing users model

    def test_creating_new_user_method(self):
        username = "brian.mutua"
        email = "bmutua@gmail.com"
        password = "Briammutua$#@!"
        result = self.user.create_user(username, email, password)
        self.assertEqual(result, [email, password])


if __name__ == "__main__":
    unittest.main()
