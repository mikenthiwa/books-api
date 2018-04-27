from flask import Flask, jsonify, request
from app.models import Books, Users
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_jwt_identity)
import re

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret'
jwt = JWTManager(app)
book = Books()
user = Users()
users = user.all_users()
books = book.get_all_books()


@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "it works"})


@app.route('/api/v1/auth/register', methods=['POST'])
def new_user():
    if not request.is_json:
        return jsonify({"msg": 'Missing json in request'})

    username = request.json.get('username', None)
    email = request.json.get('email', None)
    password = request.json.get('password', None)

    if not username and not email and not password:
        return jsonify({"msg": 'username, email, and password are empty'})
    elif not username and not password:
        return jsonify({"msg": 'username and password are empty'})
    elif not username and not email:
        return jsonify({"msg": 'username and email are empty'})
    elif not email and not password:
        return jsonify({"msg": 'email and password are empty'})
    elif not username:
        return jsonify({"msg": 'username is empty'})
    elif not email:
        return jsonify({"msg": 'email is empty'})
    elif not password:
        return jsonify({"msg": 'password is empty'})
    else:
        if not re.match(r'[A-Za-z0-9@#$%^&+=]{8,}', password):
            return jsonify({"msg": "Password should contain at least Upper case, lowercase"
                                   "number and special character"})
        else:
            user.create_user(username, email, password)
            return jsonify({"username": username, "email": email, "password": password})


@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing json in request"}), 400
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if not username and not password:
        return jsonify({"msg": 'username and password are empty'}), 200
    elif not username:
        return jsonify({"msg": 'username is empty'}), 200
    elif not password:
        return jsonify({"msg": 'password is empty'}), 200
    else:
        if username not in users:
            return jsonify({'msg': "Invalid user"}), 200
        if password != users[username][1]:
            return jsonify({"msg": 'wrong password'}), 200

        access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200


@app.route('/api/v1/books', methods=['GET'])
def all_books():
    return jsonify(book.get_all_books())


@app.route('/api/v1/users/books/<int:book_id>', methods=['GET'])
@jwt_required
def borrow(book_id):
    current_user = get_jwt_identity()
    if current_user in users:
        if book_id in books:
            borrow_book = book.get_a_book(book_id)
            print(borrow_book[2])

            return jsonify(borrow_book)

    return jsonify(logged_in_as=current_user), 200


@app.route('/api/v1/books/<int:book_id>', methods=['GET', 'PUT', 'DELETE'])
def specific_book(book_id):
    # get a specific book
    if request.method == "GET":
        return jsonify(book.get_a_book(book_id))
    # modify book info
    if request.method == 'PUT':
        if not request.is_json:
            return jsonify({"msg": "Missing json in request"}), 400
        title = request.json.get("title")
        author = request.json.get("author")
        copies = request.json.get("copies")

        if title:
            book.modify_book_title(book_id, title)
        if author:
            book.modify_book_author(book_id, author)
        if copies:
            book.modify_book_copies(book_id, copies)
        return jsonify(book.get_a_book(book_id)), 200

    # Delete a book
    if request.method == 'DELETE':
        if not request.is_json:
            return jsonify({"msg": "Missing json in request"}), 400
        book.delete_book(book_id)
        return jsonify(book.get_all_books())


@app.route('/api/v1/books', methods=['POST'])
def add_new_book():
    if not request.is_json:
        return jsonify({"msg": "Missing json in request"}), 400
    book_id = request.json.get('book_id')
    title = request.json.get('title')
    author = request.json.get('author')
    copies = request.json.get('copies')
    book.add_book(int(book_id), title, author, copies)
    return jsonify(book.get_all_books())


@app.route('/api/auth/reset-password', methods=['POST'])
def reset_password():
    if not request.is_json:
        return jsonify({"msg": "Missing json in request"}), 400
    username = request.json.get("username")
    password = request.json.get("password")
    user.change_password(username, password)
    return jsonify({"username": username, "password": password})


if __name__ == '__main__':
    app.run(debug=True, port=8000)
