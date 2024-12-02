from App.database import db
from App.models import Admin, Staff


def validate_staff(email, password):
    staff = Staff.query.filter_by(email=email).first()
    if staff and staff.check_password(password):
        return staff
    return None


def validate_admin(email, password):
    admin = Admin.query.filter_by(email=email).first()
    if admin and admin.check_password(password):
        return admin
    return None


def get_user(email, password):
    user = validate_staff(email, password)
    if user:
        return user
    user = validate_admin(email, password)
    if user:
        return user
    return None


def get_uid(email):
    user = Staff.query.filter_by(email=email).first()
    if user:
        return user.u_id
    return None
