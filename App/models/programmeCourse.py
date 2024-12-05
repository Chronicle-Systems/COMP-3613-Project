from App.database import db

class ProgrammeCourse(db.Model):
    __tablename__ = 'programme_course'

    programme_id = db.Column(db.Integer, db.ForeignKey('programme.id'), primary_key=True, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), primary_key=True, nullable=False) 
    semester_id = db.Column(db.Integer, db.ForeignKey('semester.id'), primary_key=True, nullable=False)

    # Relationships
    programme = db.relationship('Programme', back_populates='programme_courses', lazy='joined')
    semester = db.relationship('Semester', backref='programme_courses', lazy='joined')
    course = db.relationship('Course', back_populates='programme_courses', lazy='joined')

    def __init__(self, course_id: str, programme_id: int, semester_id: int):
        self.course_id = course_id
        self.programme_id = programme_id
        self.semester_id = semester_id

    def __repr__(self):
        return f"<ProgrammeCourse (Programme ID={self.programme_id}, Course ID='{self.course_id}', Semester ID={self.semester_id})>"

    def __str__(self):
        return f"ProgrammeCourse (Programme ID={self.programme_id}, Course ID={self.course_id}, Semester ID={self.semester_id})"

    def to_json(self):
        return {
            "programme_id": self.programme_id,
            "course_id": self.course_id,
            "semester_id": self.semester_id,
            "programme": self.programme.to_json() if self.programme else None,  # Optional: Add programme details
            "course": self.course.to_json() if self.course else None,  # Optional: Add course details
        }
