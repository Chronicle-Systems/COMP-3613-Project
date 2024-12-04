from App.database import db

class Course(db.Model):
    __tablename__ = 'course'

    id = db.Column(db.Integer, primary_key=True,
                   auto_increment=True, nullable=False, unique=True)
    course_code = db.Column(db.String(9), primary_key=True, unique=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(1024), nullable=False)
    credits = db.Column(db.Integer, nullable=False)
    level = db.Column(db.Integer, nullable=False)
    
    # Relationship to ProgrammeCourse
    programme_courses = db.relationship("ProgrammeCourse", back_populates="course")
    offerings = db.relationship("CourseOffering", back_populates="course")

    def __init__(self, course_code: str, name: str, description: str, credits: int, level: int):
        self.course_code = course_code
        self.name = name
        self.description = description
        self.credits = credits
        self.level = level

    def __str__(self) -> str:
        return f"""
Course Info:
    - ID: {self.id}
    - Course Code: {self.course_code}
    - Name: {self.name}
    - Description: {self.description}
    - Credits: {self.credits}
    - Level: {self.level}
"""

    def __repr__(self) -> str:
        return (f"<Course(id={self.id}, "
                f"course_code='{self.course_code}', "
                f"name='{self.name}', "
                f"description='{self.description}', "
                f"credits={self.credits}, "
                f"level={self.level})>")

    def to_json(self) -> dict:
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
    def addCourse(course_code: str, name: str, description: str, credits: int, level: int):
        newCourse = Course(course_code, name, description, credits, level)
        db.session.add(newCourse)
        db.session.commit()
        return newCourse
