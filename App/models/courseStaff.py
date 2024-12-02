from App.database import db
from .course import CourseOffering
from .staff import Staff
from datetime import date


class CourseStaff(db.Model):
    __tablename__ = 'course_staff'

    staff_id = db.Column(db.Integer, db.ForeignKey(
        'staff.id'), primary_key=True, nullable=False)
    course_offering_id = db.Column(db.Integer, db.ForeignKey(
        'course_offering.id'), primary_key=True, nullable=False)
    course_role = db.Column(db.String, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)

    # relationships
    staff = db.relationship('Staff', backref=db.backref(
        'course_staff', lazy='dynamic'))
    course_offering = db.relationship(
        'CourseOffering', backref=db.backref('course_staff', lazy='dynamic'))

    def __init__(self, staff_id: int, course_offering_id: int, course_role: str, start_date: date, end_date: date):
        self.staff_id = staff_id
        self.course_offering_id = course_offering_id
        self.course_role = course_role
        self.start_date = start_date
        self.end_date = end_date

    def __repr__(self):
        return f"<CourseStaff (Staff ID={self.staff_id}, Course Offering ID={self.course_offering_id}, Role='{self.course_role}')>"

    def __str__(self):
        return f"CourseStaff (Staff ID={self.staff_id}, Course Offering ID={self.course_offering_id}, Role={self.course_role})"

    def to_json(self):
        return {
            "staff_id": self.staff_id,
            "course_offering_id": self.course_offering_id,
            "course_role": self.course_role,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
        }

    # add new CourseStaff
    def add_course_staff(self):
        db.session.add(self)
        db.session.commit()
