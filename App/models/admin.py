from App.database import db
from .user import User

from flask_login import UserMixin, login_user


import flask_login
from App.database import db
from .user import User
from flask_login import UserMixin

class Admin(User, UserMixin):
    __tablename__ = 'admin'

    # Add the public_ID or any other fields required
    public_ID = db.Column(db.String(100), unique=True,nullable=False)
    email = db.Column(db.String(120), nullable=False)

    def __init__(self, u_ID, public_ID, password, email):
        # Assuming 'User' class requires u_ID, password, and email.
        super().__init__(u_ID, password, email)  # Call User constructor
        self.public_ID = public_ID  # Set public_ID for Admin

    def login(self):
        return flask_login.login_user(self)

    def __str__(self):
        return f"Admin (ID={self.id}, Email={self.email}, Public ID={self.public_ID})"

    def __repr__(self):
        return f"<Admin (ID={self.id}, Email='{self.email}', Public ID='{self.public_ID}')>"

    def to_json(self):
        return {
            "admin_ID": self.id,
            "email": self.email,
            "public_ID": self.public_ID  # Include public_ID in the JSON response
        }
