from App.models import Assessment
from App.database import db
from datetime import date, time
from flask_mail import Mail, Message
from flask import current_app
from App.models import Staff


def create_assessment(course_offering_id, category_id, name, status, start_date, end_date, start_time, end_time, weight):
    new_assessment = Assessment(
        course_offering_id=course_offering_id,
        category_id=category_id,
        name=name,
        status=status,
        start_date=start_date,
        end_date=end_date,
        start_time=start_time,
        end_time=end_time,
        weight=weight
    )
    db.session.add(new_assessment)
    db.session.commit()
    return new_assessment


def detect_clash(assessment):
    existing_assessments = Assessment.query.filter(
        Assessment.start_date <= assessment.end_date,
        Assessment.end_date >= assessment.start_date,
        Assessment.id != assessment.id
    ).all()
    for existing in existing_assessments:
        if existing.course_offering_id == assessment.course_offering_id:
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
    notify(assessment, clash)


def reschedule(assessment, start_date, end_date, start_time, end_time):
    assessment.start_date = start_date
    assessment.end_date = end_date
    assessment.start_time = start_time
    assessment.end_time = end_time
    db.session.commit()


def notify(assessment, clash):
    mail = Mail(current_app)
    staff = Staff.query.filter_by(id=assessment.staff_id).first()
    if not staff:
        return
    subject = f"Assessment {assessment.status}"
    recipients = [staff.email]
    if clash:
        body = f"Your assessment '{assessment.name}' has a scheduling clash."
    else:
        body = f"Your assessment '{assessment.name}' has been {assessment.status.lower()}."
    msg = Message(subject=subject, recipients=recipients, body=body)
    mail.send(msg)