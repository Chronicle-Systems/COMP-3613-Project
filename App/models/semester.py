from App.database import db
from datetime import date

class Semester(db.Model):
    __tablename__ = 'semester'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    weekly_assessment_limit = db.Column(db.Integer, nullable=False)

    # Relationship to CourseOffering
    course_offerings = db.relationship(
        'CourseOffering', back_populates='semester', lazy='dynamic'  # Use back_populates here
    )

    def __init__(self, start_date: date, end_date: date, weekly_assessment_limit: int):
        self.start_date = start_date
        self.end_date = end_date
        self.weekly_assessment_limit = weekly_assessment_limit

    def __str__(self) -> str:
        return f"""
Semester Info:
    - ID: {self.id}
    - Start Date: {str(self.start_date)}
    - End Date: {str(self.end_date)}
    - Weekly Assessment Limit: {self.weekly_assessment_limit}
"""

    def __repr__(self) -> str:
        return (f"<Semester(id={self.id}, "
                f"start_date={self.start_date}, "
                f"end_date={self.end_date}, "
                f"weekly_assessment_limit={self.weekly_assessment_limit})>")

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "weekly_assessment_limit": self.weekly_assessment_limit
        }
