from App.database import db
from enum import Enum


class ApprovalStatus(Enum):
    APPROVED = "Approved"
    PENDING = "Pending"
    REJECTED = "Rejected"


class Assessment(db.Model):
    __tablename__ = 'assessment'

    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, nullable=False)
    course_offering_id = db.Column(
        db.Integer, db.ForeignKey('courseOffering.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey(
        'category.id'), nullable=False)
    status = db.Column(db.Enum(ApprovalStatus), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    weight = db.Column(db.Float, nullable=False)

    # relationships
    course_offering = db.relationship(
        'CourseOffering', backref='assessments', lazy='joined')
    category = db.relationship(
        'Category', backref='assessments', lazy='joined')

    def __init__(self, course_offering_id: int, category_id: int, name: str, status: ApprovalStatus,
                 start_date: str, end_date: str, start_time: str, end_time: str, weight: float):
        self.course_offering_id = course_offering_id
        self.category_id = category_id
        self.name = name
        self.status = status
        self.start_date = start_date
        self.end_date = end_date
        self.start_time = start_time
        self.end_time = end_time
        self.weight = weight

    def __repr__(self):
        return f"<Assessment (ID={self.id}, Name='{self.name}', Status='{self.status}')>"

    def __str__(self):
        return f"Assessment (ID={self.id}, Name={self.name}, Status={self.status})"

    def to_json(self):
        return {
            "assessmentNo": self.id,
            "course_offering_id": self.course_offering_id,
            "category_id": self.category_id,
            "status": self.status.value,
            "name": self.name,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "weight": self.weight
        }

    # add new assessment to course
    def add_assessment(self, course_offering_id: int, category_id: int, name: str, status: ApprovalStatus,
                       start_date: str, end_date: str, start_time: str, end_time: str, weight: float):
        new_assessment = Assessment(
            course_offering_id, category_id, name, status, start_date, end_date, start_time, end_time, weight)
        db.session.add(new_assessment)  # Add to db
        db.session.commit()
        return new_assessment
