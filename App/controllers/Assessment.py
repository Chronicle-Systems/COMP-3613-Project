from App.models import Assessment, StaffObserver
from App.database import db
from datetime import date, time

def create_assessment(data):
    new_assessment = Assessment(**data)
    db.session.add(new_assessment)
    db.session.commit()
    return new_assessment

