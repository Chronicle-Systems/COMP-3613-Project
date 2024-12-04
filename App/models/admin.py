from App.database import db
from .user import User

from flask_login import UserMixin, login_user


import flask_login
from App.database import db
from .user import User
from flask_login import UserMixin


class Admin(User, UserMixin):
    __tablename__ = 'admin'

    def __init__(self, public_ID, password, email):
        super().__init__(pub, password, email)  # Call User constructor
        self.public_ID = public_ID  # Set public_ID for Admin

    def __str__(self):
        return f"""
Admin Info:
    - Public ID: {self.public_ID}
    - Email: {self.email}
"""

    def __repr__(self):
        return f"<Admin(id={self.id}, public_ID={self.public_ID}, hashed_password='*****', email='{self.email}')>"

    def to_json(self):
        return {
            "id": self.id,
            "public_ID": self.public_ID,
            "email": self.email
        }

    def login(self):
        return flask_login.login_user(self)
