from App.database import db
from .user import User

from flask_login import UserMixin, login_user


import flask_login
from App.database import db
from .user import User
from flask_login import UserMixin


class Admin(User, UserMixin):
    __tablename__ = 'admin'

    def __init__(self, public_id: int, password: str, email: str):
        super().__init__(public_id, password, email)

    def __str__(self) -> str:
        return f"""
Admin Info:
    - Public ID: {self.public_ID}
    - Email: {self.email}
"""

    def __repr__(self) -> str:
        return (f"<Admin(id={self.id}, "
                f"public_ID={self.public_ID}, "
                f"hashed_password='*****', "
                f"email='{self.email}')>")

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "public_ID": self.public_ID,
            "email": self.email
        }

    def login(self):
        return flask_login.login_user(self)
