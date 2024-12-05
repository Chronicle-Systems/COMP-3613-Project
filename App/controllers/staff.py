from App.database import db
from App.models import Staff, CourseStaff
from App.models.admin import Admin
from App.models.staff import Role


def register_staff(email, password, first_name, last_name):
    existing_user = Staff.query.filter_by(email=email).first()
    if existing_user:
        return None
        
    last_staff = Staff.query.order_by(Staff.id.desc()).first()
    new_id = (last_staff.id + 1) if last_staff else 1
 
    global_role = Role.INSTRUCTOR

    public_ID = str(new_id)  
    
    new_staff = Staff(
        first_name=first_name,
        last_name=last_name,
        id=new_id,
        public_ID=public_ID,
        global_role=global_role,
        email=email,
        password=password
    )
    
    db.session.add(new_staff)
    db.session.commit()
    return new_staff


def add_course_staff(staff_id, course_offering_id):
    existing_course_staff = CourseStaff.query.filter_by(
        staff_id=staff_id, course_offering_id=course_offering_id).first()
    if existing_course_staff:
        return existing_course_staff
    new_course_staff = CourseStaff(staff_id=staff_id, course_offering_id=course_offering_id)
    db.session.add(new_course_staff)
    db.session.commit()
    return new_course_staff


def get_registered_courses(staff_id):
    course_staff_list = CourseStaff.query.filter_by(staff_id=staff_id).all()
    codes = [item.course_offering_id for item in course_staff_list]
    return codes
