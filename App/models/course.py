from App.database import db

class Course(db.Model):
    __tablename__ = 'course'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    courseCode = db.Column(db.String(9), primary_key=True, unique=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(1024), nullable=False)
    credits = db.Column(db.Integer, nullable=False)
    level = db.Column(db.Integer, nullable=False)
    
    # Relationship to ProgrammeCourse
    programme_courses = db.relationship("ProgrammeCourse", back_populates="course")
    offerings = db.relationship("CourseOffering", back_populates="course")

    def __init__(self,id, code, name, description, credits, level):
        self.id = id
        self.courseCode = code
        self.name = name
        self.description = description
        self.credits = credits
        self.level = level

    def __str__(self):
        return f"Course (ID={self.id}, Code={self.courseCode}, Name={self.name})"

    def __repr__(self):
        return f"<Course (ID={self.id}, Code='{self.courseCode}', Name='{self.name}')>"

    def to_json(self):
        return {
            "id": self.id,
            "courseCode": self.courseCode,
            "name": self.name,
            "description": self.description,
            "credits": self.credits,
            "level": self.level,
            "offerings": [offering.to_json() for offering in self.offerings],  # Include offerings
            "programme_courses": [programme_course.to_json() for programme_course in self.programme_courses]  # Include linked ProgrammeCourses
        }

    # Add a new Course
    @staticmethod
    def addCourse(code, name, description, credits, level):
        newCourse = Course(code, name, description, credits, level)
        db.session.add(newCourse)
        db.session.commit()
        return newCourse
