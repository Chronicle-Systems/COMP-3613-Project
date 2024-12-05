from App.database import db

class CourseOffering(db.Model):
    __tablename__ = 'course_offering'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    semester_id = db.Column(db.Integer, db.ForeignKey('semester.id'), nullable=False)
    clash_detected = db.Column(db.Boolean, default=False, nullable=False)  # Add this line

    # Relationships
    course = db.relationship("Course", back_populates="offerings")
    semester = db.relationship("Semester", back_populates="course_offerings")  # Use back_populates here
    assessments = db.relationship(
        'Assessment', back_populates='course_offering', lazy='dynamic'
    )
    course_staff = db.relationship(
        'CourseStaff', back_populates='course_offering', lazy='dynamic'
    )

    def __init__(self, course_id, semester_id, clash_detected=False):
        self.course_id = course_id
        self.semester_id = semester_id
        self.clash_detected = clash_detected

    def __str__(self):
        return f"CourseOffering (ID={self.id}, Course ID={self.course_id}, Semester ID={self.semester_id})"

    def __repr__(self):
        return f"<CourseOffering (ID={self.id}, Course ID={self.course_id}, Semester ID={self.semester_id})>"

    def to_json(self):
        return {
            "id": self.id,
            "course_id": self.course_id,
            "semester_id": self.semester_id,
            "course": self.course.to_json() if self.course else None,
            "semester": self.semester.to_json() if self.semester else None,
            "assessments": [assessment.to_json() for assessment in self.assessments],
            "course_staff": [staff.to_json() for staff in self.course_staff],
        }
