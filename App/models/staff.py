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
    TA = "Teaching Assisstant"
    TUTOR = "Tutor"
    PTTUTOR = "Part-Time Tutor"

class Staff(User,UserMixin):
  __tablename__ = 'staff'
  first_name = db.Column(db.String(120), nullable=False)
  last_name = db.Column(db.String(120), nullable=False)
  cNum = db.Column(db.Integer, nullable=False, default=0) # number of courses assigned
  global_role = db.Column(db.Enum(Role), nullable = False) # role of the staff member
  course_staff = db.relationship('CourseStaff', backref='staff', lazy='joined') # relationship to CourseStaff

  def __init__(self, first_name, last_name, id, global_role, email, password):
    super().__init__(id, password, email)
    self.first_name = first_name
    self.last_name = last_name
    self.global_role = global_role

    # assign courses based on role
    if global_role in [Role.LECTURER]: # check if role is Lecturer
      self.cNum = 2
    else:
      self.cNum = 3


    # Other teaching positions for possible extension
    # if status == "Part-Time Instructor": 
    #   self.cNum = 1
    # elif status == "Instructor": 
    #   self.cNum = 2
    # elif status == "Head of Department": 
    #   self.cNum = 2  
    # elif status == "Lecturer": 
    #   self.cNum = 3
    # elif status == "Teaching Assisstant": 
    #   self.cNum = 2
    # elif status == "Tutor": 
    #   self.cNum = 2
    # else: 
    #   self.cNum = 1  #Part-Time Tutor

  def __str__(self):
     return f"Staff (ID={self.id}, Name={self.first_name} {self.last_name}, Role={self.global_role})"
  
  def __repr__(self):
      return f"<Staff (ID={self.id}, Name='{self.first_name} {self.last_name}', Role='{self.global_role}')>"


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

  # for registering a new staff member
  @staticmethod
  def register(first_name, last_name, id, global_role, email, password):
    new_staff = Staff(first_name, last_name, id, global_role, email, password)
    db.session.add(new_staff)  # Add to the database
    db.session.commit()
    return new_staff  

  def login(self):
    return flask_login.login_user(self)

    def login(self):
        return flask_login.login_user(self)
