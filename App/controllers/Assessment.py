from App.models import Assessment, StaffObserver
from App.database import db
from datetime import date, time

def create_assessment(data):
    new_assessment = Assessment(**data)
    db.session.add(new_assessment)
    db.session.commit()
    return new_assessment

def detect_clash(assessment):
    existing_assessments = Assessment.query.filter(
        Assessment.start_date <= assessment.end_date,
        Assessment.end_date >= assessment.start_date,
        Assessment.a_ID != assessment.a_ID
    ).all()
    for existing in existing_assessments:
        if existing.courseCode == assessment.courseCode:
            return True
    return False

def approve(assessment):
    assessment.status = 'Approved'
    db.session.commit()

