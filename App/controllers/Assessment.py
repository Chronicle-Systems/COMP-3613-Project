from App.models import CourseAssessment, StaffObserver
from App.database import db
from datetime import date, time


def create_assessment(course_code, a_ID, start_date, end_date, start_time, end_time, clash_detected):
    new_assessment = CourseAssessment(
        course_code, a_ID, start_date, end_date, start_time, end_time, clash_detected)
    db.session.add(new_assessment)
    db.session.commit()
    return new_assessment


def detect_clash(assessment):
    existing_assessments = CourseAssessment.query.filter(
        CourseAssessment.start_date <= assessment.end_date,
        CourseAssessment.end_date >= assessment.start_date,
        CourseAssessment.a_ID != assessment.a_ID
    ).all()
    for existing in existing_assessments:
        if existing.course_code == assessment.course_code:
            return True
    return False


def approve(assessment):
    assessment.status = 'Approved'
    db.session.commit()


def reject(assessment):
    assessment.status = 'Rejected'
    db.session.commit()
    notify_staff(assessment, None)


def notify_staff(assessment, clash):
    StaffObserver.notify(assessment, clash)


def reschedule(assessment, start_date, end_date, start_time, end_time):
    assessment.start_date = start_date
    assessment.end_date = end_date
    assessment.start_time = start_time
    assessment.end_time = end_time
    db.session.commit()
