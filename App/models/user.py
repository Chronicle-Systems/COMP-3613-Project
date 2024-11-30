from App.database import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    __abstract__ = True

    id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True, nullable=False)
    public_ID = db.Column(db.Integer, unique=True, nullable=False) 
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique = True)

    def __init__(self, id, password, email):
        self.id = id
        self.set_password(password)
        self.email = email

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)
    
    def to_json(self):
	    return {
            "id": self.id,
            "password": self.password,
            "email":self.email
        }
    
    def __str__(self):
        return f"Staff(id={self.id}, email={self.email})"
    
    def __repr__(self):
        return f"<User (id={self.id}, email='{self.email}')>"
    
    
