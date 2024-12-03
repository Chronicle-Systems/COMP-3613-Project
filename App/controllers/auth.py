from functools import wraps
from flask import jsonify
import flask_login
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    JWTManager,
    get_jwt_identity,
    verify_jwt_in_request,
)
from App.models import User, Admin, Staff, user


def authenticate(email, password):
    """Authenticate user with email and password"""
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        return user
    return None

def setup_jwt(app):
    jwt = JWTManager(app)

    @jwt.user_identity_loader 
    def user_identity_lookup(user):
        """Return the user's ID to be stored in the JWT payload"""
        if hasattr(user, 'id'):
            return user.id
        if isinstance(user, str):
            user_obj = Staff.query.filter_by(email=user).first()
            if user_obj:
                return user_obj.id
            user_obj = Admin.query.filter_by(email=user).first()
            if user_obj:
                return user_obj.id
                
        raise ValueError("User not found")

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        user = Staff.query.get(identity)
        if user:
            return user

        user = Admin.query.get(identity)
        if user:
            return user
            
        return None


def add_auth_context(app):
    @app.context_processor
    def inject_user():
        try:
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            current_user = User.query.get(user_id)
            is_authenticated = True
        except Exception as e:
            print(e)
            is_authenticated = False
            current_user = None
        return dict(is_authenticated=is_authenticated, current_user=current_user)


def identity(payload):
    return User.query.get(payload['identity'])


def login(user):
    return flask_login.login_user(user)


def logout(user):
    flask_login.logout_user()


def setup_flask_login(app):
    login_manager = flask_login.LoginManager()
    login_manager = flask_login.LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        staff = Staff.query.get(user_id)
        if staff:
            return staff
        staff = Staff.query.get(user_id)
        if staff:
            return staff

        admin = Admin.query.get(user_id)
        if admin:
            return admin
        return None


def login_required(required_class):

    def wrapper(f):

        @wraps(f)
        @jwt_required()  # Ensure JWT authentication
        def decorated_function(*args, **kwargs):
            user = required_class.query.filter_by(
                username=get_jwt_identity()).first()
            print(user.__class__, required_class,
                  user.__class__ == required_class)
            if user.__class__ != required_class:  # Check class equality
                return jsonify(error='Invalid user role'), 403
            return f(*args, **kwargs)

        return decorated_function

    return wrapper
