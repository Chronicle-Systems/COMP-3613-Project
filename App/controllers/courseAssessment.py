from App.models import CourseOffering, Assessment, Course
from App.database import db


def create_assessment(course_code, a_id, start_date, end_date, start_time, end_time, clash_detected):
    new_assessment = CourseOffering(
        course_code=course_code,
        a_id=a_id,
        start_date=start_date,
        end_date=end_date,
        start_time=start_time,
        end_time=end_time,
        clash_detected=clash_detected
    )
    db.session.add(new_assessment)
    db.session.commit()
    return new_assessment


def list_assessments():
    return Assessment.query.all()


def get_assessment_id_by_category(category):
    assessment = Assessment.query.filter_by(category=category).first()
    return assessment.a_id


def get_assessment_category_by_id(a_id):
    assessment = Assessment.query.filter_by(a_id=a_id).first()
    return assessment.category.name


def get_course_assessment_by_id(id):
    return CourseOffering.query.filter_by(id=id).first()


def get_course_assessments_by_course_code(code):
    return CourseOffering.query.filter_by(course_code=code).all()


def get_course_assessments_by_level(level):
    courses = Course.query.filter_by(level=level).all()
    assessments = []
    for c in courses:
        assessments.extend(
            get_course_assessments_by_course_code(c.course_code))
    return assessments


def delete_course_assessment(course_assessment):
    db.session.delete(course_assessment)
    db.session.commit()
    return True


def get_clashes():
    return CourseOffering.query.filter_by(clash_detected=True).all()
