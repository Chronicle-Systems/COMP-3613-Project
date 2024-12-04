from App.database import db
from .user import User

from flask_login import UserMixin, login_user


import flask_login
from App.database import db
from .user import User
from flask_login import UserMixin


class Admin(User, UserMixin):
    __tablename__ = 'admin'

    def __init__(self, email: str, password: str):
        super().__init__(email, password)

    def __str__(self) -> str:
        return f"""
Admin Info:
    - Public ID: {self.public_ID}
    - Email: {self.email}
"""

    def __repr__(self) -> str:
        return (f"<Admin(id={self.id}, "
                f"email='{self.email}', "
                f"hashed_password='*****')>")

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "email": self.email
        }

    def login(self):
        return flask_login.login_user(self)
