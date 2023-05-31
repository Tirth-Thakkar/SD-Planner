""" database dependencies to support sqliteDB examples """
from random import randrange
from datetime import date
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash


''' Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into Python shell and follow along '''


# Define the User class to manpassword actions in the 'users' table
# -- Object Relational Mapping (ORM) is the key concept of SQLAlchemy
# -- a.) db.Model is like an inner layer of the onion in ORM
# -- b.) User represents data we want to store, something that is built on db.Model
# -- c.) SQLAlchemy ORM is layer on top of SQLAlchemy Core, then SQLAlchemy engine, SQL
class Login(db.Model):
    __tablename__ = 'logins'  # table name is plural, class name is singular

    # Define the User schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _email = db.Column(db.String(255), unique=True, nullable=False)
    _password = db.Column(db.String(255), unique=False, nullable=False)
    
    

    # constructor of a User object, initializes the instance variables within object (self)
    def __init__(self, email="tester@gmail.com", password="123test"):
       # variables with self prefix become part of the object, 
        self._email= email
        self._password = password

    # a getter method, extracts email from object
    @property
    def email(self):
        return self._email
    
    # a setter function, allows name to be updated after initial object creation
    @email.setter
    def email(self, email):
        self._email = email

    # a getter method, extracts email from object
    @property
    def password(self):
        return self._password
    
    # a setter function, allows name to be updated after initial object creation
    @password.setter
    def password(self, password):
        self._password = password
    
    # output content using str(object) in human readable form, uses getter
    # output content using json dumps, this is ready for API response
    def __str__(self):
        return json.dumps(self.read())

    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a person object from User(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "id": self.id,
            "email": self.email,
            "password": self.password,
        }

    # CRUD update: updates user name, password, phone
    # returns self
    def update(self, email="",password=""):
        """only updates values with length"""
        if len(email) > 0:
            self.email = email
        if len(password) > 0:
            self.password(password)
        db.session.commit()
        return self

    # CRUD delete: remove self
    # None
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None


"""Database Creation and Testing """


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
                '''fails with bad or duplicate data'''

                db.session.remove()
                print(f"Records exist, duplicate email, or error: {login.email}")
                
