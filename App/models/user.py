from App.database import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, nullable=False, unique=True, )
    public_id = db.Column(db.Integer, nullable=False, unique=True)
    hashed_password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)

    def __init__(self, public_id: int, password: str, email: str):
        self.public_id = public_id
        self.set_password(password)
        self.email = email

    def __str__(self) -> str:
        return f"""
Staff Info:
    - ID: {self.id}
    - Public ID: {self.public_ID}
    - Email: {self.email}
"""

    def __repr__(self) -> str:
        return (f"<User(id={self.id}, "and
                f"public_ID={self.public_ID}, "
                f"hashed_password='*****', "
                f"email='{self.email}')>")

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "public_id": self.public_ID,
            "email": self.email
        }

    def set_password(self, password: str):
        self.password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)
