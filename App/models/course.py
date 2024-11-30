from App.database import db


class Course(db.Model):
    __tablename__ = 'course'

  id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
  code = db.Column(db.String(9), primary_key=True, unique=True)
  name = db.Column(db.String(120), nullable=False)
  description = db.Column(db.String(1024), nullable=False)
  credits = db.Column(db.Integer, nullable=False)
  level = db.Column(db.Integer, nullable=False)
  offerings = db.reationship('CourseOfferings', backref='course', lazy='dynamic')

  def __init__(self, code, name, description, credits, level):
    self.code = code
    self.name = name
    self.description = description
    self.credits = credits
    self.level = level

  def __str__(self):
    return f"Course (ID={self.id}, Code={self.code}, Name={self.name})"

  def __repr__(self):
    return f"<Course (ID={self.id}, Code='{self.code}', Name='{self.name}')>"

  def to_json(self):
    return {
      "id": self.id,
      "code": self.code,
      "name": self.name,
      "description": self.description,
      "credits": self.credits,
      "level": self.level,
      "offerings": [offering.to_json() for offering in self.offerings],  # include offerings in JSON
    }

  # add new Course
  def addCourse(code, name, description, credits, level):
    newCourse = Course(code, name, description, credits, level)
    db.session.add(newCourse)
    db.session.commit()
    return newCourse
