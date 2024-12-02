from App.database import db
from App.models import Semester


def create_semester(start_date, end_date, semester_number, max_assessments):
    semester = Semester(
        start_date=start_date,
        end_date=end_date,
        semester_number=semester_number,
        max_assessments=max_assessments
    )
    db.session.add(semester)
    db.session.commit()
    return semester
