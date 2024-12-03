from App.database import db

class Semester(db.Model):
    __tablename__ = 'semester'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    semester_number = db.Column(db.Integer, nullable=False)
    weekly_assessment_limit = db.Column(db.Integer, nullable=False)

    # Relationship to CourseOffering
    course_offerings = db.relationship(
        'CourseOffering', back_populates='semester', lazy='dynamic'  # Use back_populates here
    )

    def __init__(self, start_date, end_date, semester_number, weekly_assessment_limit):
        self.start_date = start_date
        self.end_date = end_date
        self.semester_number = semester_number
        self.weekly_assessment_limit = weekly_assessment_limit

    def __str__(self):
        return f"Semester (ID={self.id}, Start Date={self.start_date}, End Date={self.end_date})"

    def __repr__(self):
        return f"<Semester (ID={self.id}, Start Date='{self.start_date}', End Date='{self.end_date}')>"

    def to_json(self):
        return {
            "id": self.id,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "weekly_assessment_limit": self.weekly_assessment_limit,
            "offered_courses": [course.to_json() for course in self.course_offerings]
        }
