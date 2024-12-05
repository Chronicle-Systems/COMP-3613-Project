from App.models import Course
from App.database import db


def add_course(course_code, course_title, description, level, semester, a_num):
    course = Course.query.filter_by(courseCode=course_code).first()
    if course:
        return course
    new_course = Course(
        courseCode=course_code,
        name=course_title,
        description=description,
        level=int(level),
        credits=int(semester)  # Using semester as credits
    )
    db.session.add(new_course)
    db.session.commit()
    return new_course


def list_courses():
    return Course.query.all()


def get_course(course_code):
    return Course.query.filter_by(courseCode=course_code).first()


def delete_course(course):
    db.session.delete(course)
    db.session.commit()
    return True


def edit_review(review, staff, is_positive=None, comment=None):
    if review.reviewer != staff:
        return None

    if is_positive is not None:
        review.isPositive = is_positive
# hoping and praying this works fr
    if comment is not None:
        review.comment = comment

    db.session.add(review)
    db.session.commit()
    return review
