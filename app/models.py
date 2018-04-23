
class Books:
    books = {1: [{"Title": "Harry Potter", "Author": "J.K.Rowling", "Copies": 3}],
             2: [{"Title": "The whistler", "Author": "John Grisham", "Copies": 3}]}

    def get_all_books(self):
        return self.books

    def get_a_book(self, book_id):
        int(book_id)
        return self.books.get(book_id, "{} does not exist".format(book_id))

    def borrow_book(self, book_id):
        int(book_id)
        return self.books.get(book_id)

    def add_book(self, book_id, book_title, author, copies):
        self.books[book_id] = [{"Title": book_title, "Author": author, "Copies": copies}]
        return self.books

    def delete_book(self, book_id):
        del self.books[book_id]
        return self.books

    def modify_book_title(self, book_id, title):
        title_book = self.books[book_id][0]
        title_book["Title"] = title
        return self.books.get(book_id)

    def modify_book_author(self, book_id, author):
        author_book = self.books[book_id][0]
        author_book["Author"] = author
        return self.books.get(book_id)

    def modify_book_copies(self, book_id, copies):
        copies_book = self.books[book_id][0]
        copies_book["Copies"] = copies
        return self.books.get(book_id)


class Users:
    users = {"mike.nthiwa": ["mike.nthiwa@gmail.com", 123456789],
             "chris.mutua": ["c.mutua@gmail.com", 789456123]}

    def create_user(self, username, email, password):
        self.users[username] = [email, password]

    def all_users(self):
        return self.users

    def change_password(self, username, password):
        self.users[username][1] = password

