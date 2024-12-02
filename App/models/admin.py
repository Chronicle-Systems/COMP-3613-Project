from App.database import db
from .user import User

from flask_login import UserMixin, login_user


class Admin(User, UserMixin):
    __tablename__ = 'admin'

    def login(self):
        return flask_login.login_user(self)

    def __init__(self, u_ID, password, email):
        super().__init__(u_ID, password, email)

    def __str__(self):
        return f"Admin (ID={self.id}, Email={self.email})"

    def __repr__(self):
        return f"<Admin (ID={self.id}, Email='{self.email}')>"

    def to_json(self):
        return {
            "admin_ID": self.id,
            "email": self.email
        }
