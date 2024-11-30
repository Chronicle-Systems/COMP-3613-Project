from App.models import Course
from App.database import db

def add_course(course_code, course_title, description, level, semester, a_num):
    # Check if course_code is already in db ie. course was already added
    course = Course.query.get(course_code)
    if course:
        return course
    else:
        # Add new Course
        new_course = Course(
            course_code=course_code,
            course_title=course_title,
            description=description,
            level=level,
            semester=semester,
            a_num=a_num
        )
        db.session.add(new_course)
        db.session.commit()
        return new_course

def list_courses():
    return Course.query.all()

def get_course(course_code):
    return Course.query.filter_by(course_code=course_code).first()

def delete_course(course):
    db.session.delete(course)
    db.session.commit()
    return True

def edit_review(review, staff, is_positive=None, comment=None):
    if review.reviewer != staff:
        return None
    
    if is_positive is not None:
        review.isPositive = is_positive
#hoping and praying this works fr
    if comment is not None:
        review.comment = comment

    db.session.add(review)
    db.session.commit()
    return review
