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
    cNum = db.Column(db.Integer, nullable=False, default=0)  # Number of courses assigned
    global_role = db.Column(db.Enum(Role), nullable=False)

    public_ID = db.Column(db.String(100), unique=True,nullable=False)

    # Relationship to CourseStaff
    course_staff = db.relationship(
        'CourseStaff', back_populates='staff', lazy='dynamic'
    )

    def __init__(self, first_name, last_name, id, public_ID, global_role, email, password):
        super().__init__(id, password, email)
        self.first_name = first_name
        self.last_name = last_name
        self.global_role = global_role

        self.public_ID = public_ID

        # Assign courses based on role
        self.cNum = 2 if global_role == Role.LECTURER else 3

    def __repr__(self):
        return f"<Staff (ID={self.id}, Name='{self.first_name} {self.last_name}', Role='{self.global_role}')>"

    def __str__(self):
        return f"Staff (ID={self.id}, Name={self.first_name} {self.last_name}, Role={self.global_role})"

    def to_json(self):
        return {
            "staff_ID": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "global_role": self.global_role.value,
            "email": self.email,
            "coursesNum": self.cNum,
            "coursesAssigned": [course.to_json() for course in self.course_staff]
        }

    @staticmethod
    def register(first_name, last_name, id, public_ID, global_role, email, password):
        new_staff = Staff(first_name, last_name, id, public_ID, global_role, email, password)
        db.session.add(new_staff)
        db.session.commit()
        return new_staff

    def login(self):
        return flask_login.login_user(self)

