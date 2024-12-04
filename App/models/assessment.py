from App.database import db
from enum import Enum

class ApprovalStatus(Enum):
    APPROVED = "Approved"
    PENDING = "Pending"
    REJECTED = "Rejected"

class Assessment(db.Model):
    __tablename__ = 'assessment'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    course_offering_id = db.Column(
        db.Integer, db.ForeignKey('course_offering.id'), nullable=False
    )
    category_id = db.Column(
        db.Integer, db.ForeignKey('category.id'), nullable=False
    )
    status = db.Column(db.Enum(ApprovalStatus), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    allow_same_level = db.Column(db.Boolean, default=False)
    max_weekly_clashes = db.Column(db.Integer, default=3)
    excluded_types = db.Column(db.String(200))  # Comma-separated a_IDs

    # relationships
    course_offering = db.relationship(
        'CourseOffering', back_populates='assessments', lazy='joined'
    )
    category = db.relationship('Category', backref=db.backref('assessments', lazy='dynamic'))

    def __init__(self, course_offering_id: int, category_id: int, name: str, status: ApprovalStatus,
                 start_date, end_date, start_time, end_time, weight: float):
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
            "start_date": str(self.start_date),
            "end_date": str(self.end_date),
            "start_time": str(self.start_time),
            "end_time": str(self.end_time),
            "weight": self.weight
        }

    @staticmethod
    def add_assessment(course_offering_id: int, category_id: int, name: str, status: ApprovalStatus,
                       start_date, end_date, start_time, end_time, weight: float):
        new_assessment = Assessment(
            course_offering_id, category_id, name, status, start_date, end_date, start_time, end_time, weight
        )
        db.session.add(new_assessment)
        db.session.commit()
        return new_assessment
