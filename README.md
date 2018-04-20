# books-api

Hello-Books is a simple api that helps manage a library and its processes like stocking,
tracking and renting books. With this application users are able to find and rent books.
The application also has an admin section where the admin can do things like add books, delete books,
increase the quantity of a book etc.


## Getting Started

Go to https://github.com/mikenthiwa/books-api.
Download or clone the repository to your local machine.
Open the project using your ide.


### Prerequisite

Python 3 and above.
Virtual environment.
Flask
flask_jwt_ext
Postman
Browser e.g Chrome, firefox, safari


### Installing

Python 3:
Download python 3 from https://www.python.org/downloads/
* On Windows :
    Run the set-up


Virtual environment:
* on windows :
    Open cmd.
    Navigate to the project.
    Create the virtual environment
        * virtualenv env.
    Activate the virtual environment:
        * cd: env\scripts\activate.
    Install the following modules within the virtual environment
    Flask module:
        * pip install flask.
    jwt
        * pip install  flask_jwt_extended.
    nose
        * pip install nose


## Running the test
* on windows :
    Open git bash
    In git bash run
        * nosetests tests.test_book.py








