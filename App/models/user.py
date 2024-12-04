from App.database import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, nullable=False, unique=True, )   # Internal ID (should technically be private)
    #public_id = db.Column(db.Integer, nullable=False, unique=True)     # Public ID (8160.....); removing for now for simplicity
    hashed_password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)

    def __init__(self, email: str, password: str):
        self.email = email
        self.set_password(password)

    def __str__(self) -> str:
        return f"""
Staff Info:
    - ID: {self.id}
    - Email: {self.email}
"""

    def __repr__(self) -> str:
        return (f"<User(id={self.id}, "
                f"email='{self.email}"
                f"hashed_password='*****')>")

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "email": self.email
        }

    def set_password(self, password: str):
        self.password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)
