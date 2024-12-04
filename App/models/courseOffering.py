from App.database import db

class CourseOffering(db.Model):
    __tablename__ = 'course_offering'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    semester_id = db.Column(db.Integer, db.ForeignKey('semester.id'), nullable=False)

    # Relationships
    course = db.relationship("Course", back_populates="offerings")
    semester = db.relationship("Semester", back_populates="course_offerings")  # Use back_populates here
    assessments = db.relationship(
        'Assessment', back_populates='course_offering', lazy='dynamic'
    )
    course_staff = db.relationship(
        'CourseStaff', back_populates='course_offering', lazy='dynamic'
    )

    def __init__(self, course_id, semester_id):
        self.course_id = course_id
        self.semester_id = semester_id

    def __str__(self):
        return f"""
CourseOffering Info:
    - ID: {self.id}
    - Course ID: {self.course_id}
    - Semester ID:{self.semester_id}
"""

    def __repr__(self):
        return (f"<CourseOffering (id={self.id}, "
                f"course_id={self.course_id}, "
                f"semester_id={self.semester_id})>")

    def to_json(self):
        return {
            "id": self.id,
            "course_id": self.course_id,
            "semester_id": self.semester_id,
        }
