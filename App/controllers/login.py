from App.models import Admin
from App.database import db
from App.models.staff import Staff


def login_admin(email, password):
    admin = db.session.query(Admin).filter(Admin.u_ID == email).first()
    if admin != None:
        if admin.check_password(password):
            return admin.login()
    return "Login failed"


def login_staff(email, password):
    staff = db.session.query(Staff).filter(Staff.email == email).first()
    if staff != None:
        if staff.check_password(password):
            return staff.login()
    return "Login failed"
