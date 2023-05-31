from random import randrange
from datetime import date
import os
import base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

# Define the Login class to manage user login actions in the 'logins' table
class Login(db.Model):
    __tablename__ = 'logins'  # table name is plural, class name is singular

    # Define the Login schema with variables from the object
    id = db.Column(db.Integer, primary_key=True)
    _email = db.Column(db.String(255), unique=True, nullable=False)
    _password = db.Column(db.String(255), unique=False, nullable=False)

    # Constructor of a Login object, initializes the instance variables within the object (self)
    def __init__(self, email, password):
        self._email = email
        self._password = password

    # Getter method to retrieve email from the object
    @property
    def email(self):
        return self._email

    # Setter function to update the email after initial object creation
    @email.setter
    def email(self, email):
        self._email = email

    # Getter method to retrieve password from the object
    @property
    def password(self):
        return self._password

    # Setter function to update the password after initial object creation
    @password.setter
    def password(self, password):
        self._password = password

    # Output content using str(object) in human-readable form
    def __str__(self):
        return json.dumps(self.read())

    # CRUD create/add a new record to the table
    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read converts self to a dictionary
    def read(self):
        return {
            "id": self.id,
            "email": self.email,
            "password": self.password,
        }

    # CRUD update: updates user email and password
    def update(self, email="", password=""):
        """Only updates values with length"""
        if len(email) > 0:
            self.email = email
        if len(password) > 0:
            self.password = password
        db.session.commit()
        return self

    # CRUD delete: remove self
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None


"""Database Creation and Testing"""


# Builds working data for testing
def initLogins():
    with app.app_context():
        """Create database and tables"""
        db.init_app(app)
        db.create_all()

        """Tester data for table"""
        u1 = Login(email="jishnu@gmail.com", password='123jishnu')
        u2 = Login(email="alan@gmail.com", password='123alan')
        u3 = Login(email="tirth@gmail.com", password='123tirth')
        u4 = Login(email="yuri@gmail.com", password='123yuri')
        u5 = Login(email="haoxuan@gmail.com", password='123haoxuan')

        logins = [u1, u2, u3, u4, u5]

        """Builds sample user/note(s) data"""
        for login in logins:
            try:
                login.create()
            except IntegrityError:
                '''Fails with bad or duplicate data'''
                db.session.remove()
                print(f"Records exist, duplicate email, or error: {login.email}")
