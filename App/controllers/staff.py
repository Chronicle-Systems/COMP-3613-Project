from App.database import db
from App.models import Staff, CourseStaff
from App.models.admin import Admin


def register_staff(first_name, last_name, u_id, status, email, password):
    # Check if staff already exists
    existing_staff = Staff.query.filter_by(email=email).first()
    if existing_staff:
        return None
    new_staff = Staff(
        first_name=first_name,
        last_name=last_name,
        u_id=u_id,
        status=status,
        email=email
    )
    new_staff.set_password(password)
    db.session.add(new_staff)
    db.session.commit()
    return new_staff

def add_course_staff(u_id, course_code):
    existing_course_staff = CourseStaff.query.filter_by(
        u_id=u_id, course_code=course_code).first()
    if existing_course_staff:
        return existing_course_staff
    new_course_staff = CourseStaff(u_id=u_id, course_code=course_code)
    db.session.add(new_course_staff)
    db.session.commit()
    return new_course_staff

def get_registered_courses(u_id):
    course_staff_list = CourseStaff.query.filter_by(u_id=u_id).all()
    codes = [item.course_code for item in course_staff_list]
    return codes
