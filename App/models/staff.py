import flask_login
from App.database import db
from .user import User
import enum
from flask_login import UserMixin


class Role(enum.Enum):
    PTINSTRUCT = "Part-Time Instructor"
    INSTRUCTOR = "Instructor"
    HOD = "Head of Department"
    LECTURER = "Lecturer"
    TA = "Teaching Assistant"
    TUTOR = "Tutor"
    PTTUTOR = "Part-Time Tutor"


class Staff(User, UserMixin):
    __tablename__ = 'staff'
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    global_role = db.Column(db.Enum(Role), nullable=False)
    # cNum = db.Column(db.Integer, nullable=False, default=0)  # Number of courses assigned

    course_staff = db.relationship(
        'CourseStaff', back_populates='staff', lazy='dynamic'
    )

    def __init__(self, email: str, password: str, first_name: str, last_name: str, global_role: Role):
        super().__init__(email, password)
        self.first_name = first_name
        self.last_name = last_name
        self.global_role = global_role

        # Assign courses based on role
        # self.cNum = 2 if global_role == Role.LECTURER else 3

    def __str__(self) -> str:
        return f"""
Staff Info:
    - ID: {self.id}
    - Email: {self.email}
    - First Name: {self.first_name}
    - Last Name: {self.last_name}
    - Global Role: {self.global_role.value}
"""

    def __repr__(self) -> str:
        return (f"<Admin(id={self.id}, "
                f"email='{self.email}', "
                f"hashed_password='*****', "
                f"first_name='{self.first_name}', "
                f"last_name='{self.last_name}', "
                f"global_role='{self.global_role.value}')>")

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "global_role": self.global_role.value
        }

    @staticmethod
    def register(email: str, password: str, first_name: str, last_name: str, global_role: Role):
        new_staff = Staff(email, password, first_name, last_name, global_role)
        db.session.add(new_staff)
        db.session.commit()
        return new_staff

    def login(self):
        return flask_login.login_user(self)
