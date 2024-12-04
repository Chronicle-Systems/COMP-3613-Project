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

    def __init__(self, public_id, password, email, first_name, last_name, global_role):
        super().__init__(public_id, password, email)
        self.first_name = first_name
        self.last_name = last_name
        self.global_role = global_role

        # Assign courses based on role
        # self.cNum = 2 if global_role == Role.LECTURER else 3

    def __str__(self):
        return f"""
Staff Info:
    - Public ID: {self.public_id}
    - Email: {self.email}
    - First Name: {self.first_name}
    - Last Name: {self.last_name}
    - Global Role: {self.global_role.value}
"""

    def __repr__(self):
        return f"<Admin(id={self.id}, public_ID={self.public_ID}, hashed_password='*****', email='{self.email}', first_name='{self.first_name}', last_name='{self.last_name}', global_role='{self.global_role.value}')>"

    def to_json(self):
        return {
            "id": self.id,
            "public_id": self.public_id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "global_role": self.global_role.value,
            "courses_assigned": [course.to_json() for course in self.course_staff]
        }

    @staticmethod
    def register(public_id, password, email, first_name, last_name, global_role):
        new_staff = Staff(public_id, password, email, first_name, last_name, global_role)
        db.session.add(new_staff)
        db.session.commit()
        return new_staff

    def login(self):
        return flask_login.login_user(self)
