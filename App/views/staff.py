from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, get_flashed_messages, session
from flask_login import current_user
from flask import current_app as app
from flask_mail import Mail, Message
from sqlalchemy import not_
from App.controllers import staff
from App.controllers import Course, semester
from App.controllers import Assessment
from App.database import db
from App.models.assessment import Assessment
import json
from flask_jwt_extended import current_user as jwt_current_user, get_jwt_identity
from flask_jwt_extended import jwt_required
from datetime import date, timedelta
import time

from App.controllers.staff import (
    register_staff,
    add_course_staff,
    get_registered_courses,
)
from App.controllers.login import (
    login_staff
)

from App.controllers.course import (
    list_courses
)

from App.controllers.user import (
    get_uid
)

from App.controllers.courseAssessment import (
    create_assessment,
    list_assessments,
    get_assessment_id_by_category,
    get_assessment_category_by_id,
    get_course_assessment_by_id,
    get_course_assessments_by_course_code,
    get_course_assessments_by_level,
    delete_course_assessment,
    get_clashes
)

staff_views = Blueprint('staff_views', __name__,
                        template_folder='../templates')

# Gets Signup Page


@staff_views.route('/signup', methods=['GET'])
def get_signup_page():
    return render_template('signup.html')

# Gets Calendar Page


@staff_views.route('/calendar', methods=['GET'])
@jwt_required()
def get_calendar_page():
    id = get_uid(get_jwt_identity())  # gets u_id from email token

    # Get courses for filter
    courses = []
    allCourses = [course.courseCode for course in list_courses()]
    myCourses = get_registered_courses(id)
    for course in allCourses:
        if course not in myCourses:
            courses.append(course)

    # Get assessments for registered courses
    all_assessments = []
    for course in myCourses:
        all_assessments = all_assessments + get_course_assessments_by_course_code(course)

    # Format assessments for calendar js - registered courses
    myAssessments = []
    for item in all_assessments:
        obj = format_assessment(item)
        myAssessments.append(obj)

    # Get assessments for all other courses (for filters)
    other_assessments = []
    for c in courses:
        other_assessments = other_assessments + get_course_assessments_by_course_code(c)

    # Format assessments for calendar js - filters
    assessments = []
    for item in other_assessments:
        if not item.clashDetected:
            obj = format_assessment(item)
            assessments.append(obj)

    # Ensure courses, myCourses, and assessments are not empty
    if not courses:
        courses = []
    if not myCourses:
        myCourses = []
    if not myAssessments:
        myAssessments = []
    if not assessments:
        assessments = []

    sem = semester.query.order_by(semester.id.desc()).first()
    semester_obj = {'start': sem.startDate, 'end': sem.endDate}

    messages = []
    message = session.pop('message', None)
    if message:
        messages.append(message)
    return render_template('index.html', courses=courses, myCourses=myCourses, assessments=myAssessments, semester=semester_obj, otherAssessments=assessments, messages=messages)


def format_assessment(item):
    if item.startDate is None:
        obj = {'courseCode': item.courseCode,
               'a_ID': get_assessment_category_by_id(item.a_ID),
               'caNum': item.id,
               'startDate': item.startDate,
               'endDate': item.endDate,
               'startTime': item.startTime,
               'endTime': item.endTime,
               'clashDetected': item.clashDetected
               }
    else:
        obj = {'courseCode': item.courseCode,
               'a_ID': get_assessment_category_by_id(item.a_ID),
               'caNum': item.id,
               'startDate': item.startDate.isoformat(),
               'endDate': item.endDate.isoformat(),
               'startTime': item.startTime.isoformat(),
               'endTime': item.endTime.isoformat(),
               'clashDetected': item.clashDetected
               }
    return obj


@staff_views.route('/calendar', methods=['POST'])
@jwt_required()
def update_calendar_page():
    # Retrieve data from page
    id = request.form.get('id')
    startDate = request.form.get('startDate')
    startTime = request.form.get('startTime')
    endDate = request.form.get('endDate')
    endTime = request.form.get('endTime')

    # Get course assessment
    assessment = get_course_assessment_by_id(id)
    if assessment:
        assessment.startDate = startDate
        assessment.endDate = endDate
        assessment.startTime = startTime
        assessment.endTime = endTime

        db.session.commit()

        clash = detect_clash(assessment.id)
        if clash:
            assessment.clashDetected = True
            db.session.commit()
            session['message'] = assessment.courseCode + \
                " - Clash detected! The maximum amount of assessments for this level has been exceeded."
        else:
            session['message'] = "Assessment modified"
    return session['message']


def detect_clash(id):
    clash = 0
    # get the weekly max num of assessments allowed per level
    sem = semester.query.order_by(semester.id.desc()).first()
    max_assessments = sem.maxAssessments
    new_assessment = get_course_assessment_by_id(id)  # get current assessment info
    compare_code = new_assessment.courseCode.replace(' ', '')
    all_assessments = Assessment.query.filter(
        not_(Assessment.a_ID.in_([2, 4, 8]))).all()
    if not new_assessment.endDate:  # dates not set yet
        return False
    relevant_assessments = []
    for a in all_assessments:
        code = a.courseCode.replace(' ', '')
        # courses are in the same level
        if (code[4] == compare_code[4]) and (a.id != new_assessment.id):
            if a.startDate is not None:  # assessment has been scheduled
                relevant_assessments.append(a)

    sunday, saturday = get_week_range(new_assessment.endDate.isoformat())
    for a in relevant_assessments:
        dueDate = a.endDate
        if sunday <= dueDate <= saturday:
            clash = clash+1

    return clash >= max_assessments


def get_week_range(iso_date_str):
    date_obj = date.fromisoformat(iso_date_str)
    day_of_week = date_obj.weekday()

    if day_of_week != 6:
        days_to_subtract = (day_of_week + 1) % 7
    else:
        days_to_subtract = 0

    sunday_date = date_obj - \
        timedelta(days=days_to_subtract)  # get sunday's date
    saturday_date = sunday_date + timedelta(days=6)  # get saturday's date
    return sunday_date, saturday_date

# Sends confirmation email to staff upon registering


@staff_views.route('/send_email', methods=['GET', 'POST'])
def send_email():
    mail = Mail(app)  # Create mail instance

    subject = 'Test Email!'
    receiver = request.form.get('email')
    body = 'Successful Registration'

    msg = Message(subject, recipients=[receiver], html=body)
    mail.send(msg)
    return render_template('login.html')

# Retrieves staff info and stores it in database ie. register new staff


@staff_views.route('/register', methods=['POST'])
def register_staff_action():
    if request.method == 'POST':
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        staffID = request.form.get('staffID')
        status = request.form.get('status')
        email = request.form.get('email')
        pwd = request.form.get('password')

        # Field Validation is on HTML Page!
        register_staff(firstName, lastName, staffID, status, email, pwd)
        return render_template('login.html')
        # return redirect(url_for('staff_views.send_email'))

# Gets account page


@staff_views.route('/account', methods=['GET'])
@jwt_required()
def get_account_page():
    id = get_uid(get_jwt_identity())  # gets u_id from email token
    courses = list_courses()
    registered_courses = get_registered_courses(id)
    return render_template('account.html', courses=courses, registered=registered_courses)

# Assign course to staff


@staff_views.route('/account', methods=['POST'])
@jwt_required()
def get_selected_courses():
    courses = list_courses()
    id = get_uid(get_jwt_identity())  # gets u_id from email token

    if request.method == 'POST':
        course_codes_json = request.form.get('courseCodes')
        course_codes = json.loads(course_codes_json)
        for code in course_codes:
            obj = add_course_staff(id, code)  # add course to course-staff table

    return redirect(url_for('staff_views.get_account_page'))

# Gets assessments page


@staff_views.route('/assessments', methods=['GET'])
@jwt_required()
def get_assessments_page():
    id = get_uid(get_jwt_identity())  # gets u_id from email token
    registered_courses = get_registered_courses(id)  # get staff's courses

    assessments = []
    for course in registered_courses:
        # get assessments by course code
        for assessment in get_course_assessments_by_course_code(course):
            if assessment.startDate is None:
                obj = {'id': assessment.id,
                       'courseCode': assessment.courseCode,
                       # convert a_ID to category value
                       'a_ID': get_assessment_category_by_id(assessment.a_ID),
                       'startDate': assessment.startDate,
                       'endDate': assessment.endDate,
                       'startTime': assessment.startTime,
                       'endTime': assessment.endTime,
                       'clashDetected': assessment.clashDetected
                       }
            else:
                obj = {'id': assessment.id,
                       'courseCode': assessment.courseCode,
                       # convert a_ID to category value
                       'a_ID': get_assessment_category_by_id(assessment.a_ID),
                       'startDate': assessment.startDate.isoformat(),
                       'endDate': assessment.endDate.isoformat(),
                       'startTime': assessment.startTime.isoformat(),
                       'endTime': assessment.endTime.isoformat(),
                       'clashDetected': assessment.clashDetected
                       }
            assessments.append(obj)  # add object to list of assessments

    return render_template('assessments.html', courses=registered_courses, assessments=assessments)

# Gets add assessment page


@staff_views.route('/addAssessment', methods=['GET'])
@jwt_required()
def get_add_assessments_page():
    id = get_uid(get_jwt_identity())  # gets u_id from email token
    registered_courses = get_registered_courses(id)
    allAsm = list_assessments()
    return render_template('addAssessment.html', courses=registered_courses, assessments=allAsm)

# Retrieves assessment info and creates new assessment for course


@staff_views.route('/addAssessment', methods=['POST'])
@jwt_required()
def add_assessments_action():
    course = request.form.get('myCourses')
    asmType = request.form.get('AssessmentType')
    startDate = request.form.get('startDate')
    endDate = request.form.get('endDate')
    startTime = request.form.get('startTime')
    endTime = request.form.get('endTime')

    if startDate == '' or endDate == '' or startTime == '' or endTime == '':
        startDate = None
        endDate = None
        startTime = None
        endTime = None

    newAsm = create_assessment(course, asmType, startDate,
                               endDate, startTime, endTime, False)
    if newAsm.startDate:
        clash = detect_clash(newAsm.id)
        if clash:
            newAsm.clashDetected = True
            db.session.commit()
            flash(
                "Clash detected! The maximum amount of assessments for this level has been exceeded.")
            time.sleep(1)

    return redirect(url_for('staff_views.get_assessments_page'))


# Modify selected assessment
@staff_views.route('/modifyAssessment/<string:id>', methods=['GET'])
def get_modify_assessments_page(id):
    allAsm = list_assessments()  # get assessment types
    assessment = get_course_assessment_by_id(id)  # get assessment details
    return render_template('modifyAssessment.html', assessments=allAsm, ca=assessment)

# Gets Update assessment Page


@staff_views.route('/modifyAssessment/<string:id>', methods=['POST'])
def modify_assessment(id):
    if request.method == 'POST':
        # get form details
        course = request.form.get('myCourses')
        asmType = request.form.get('AssessmentType')
        startDate = request.form.get('startDate')
        endDate = request.form.get('endDate')
        startTime = request.form.get('startTime')
        endTime = request.form.get('endTime')

        # update record
        assessment = get_course_assessment_by_id(id)
        if assessment:
            assessment.a_ID = asmType
            if startDate != '' and endDate != '' and startTime != '' and endTime != '':
                assessment.startDate = startDate
                assessment.endDate = endDate
                assessment.startTime = startTime
                assessment.endTime = endTime

            db.session.commit()

            clash = detect_clash(assessment.id)
            if clash:
                assessment.clashDetected = True
                db.session.commit()
                flash(
                    "Clash detected! The maximum amount of assessments for this level has been exceeded.")
                time.sleep(1)

    return redirect(url_for('staff_views.get_assessments_page'))

# Delete selected assessment


@staff_views.route('/deleteAssessment/<string:caNum>', methods=['GET'])
def delete_assessment(caNum):
    courseAsm = get_course_assessment_by_id(caNum)  # Gets selected assessment for course
    delete_course_assessment(courseAsm)
    print(caNum, ' deleted')
    return redirect(url_for('staff_views.get_assessments_page'))

# Get settings page


@staff_views.route('/settings', methods=['GET'])
@jwt_required()
def get_settings_page():
    return render_template('settings.html')

# Route to change password of user


@staff_views.route('/settings', methods=['POST'])
@jwt_required()
def changePassword():

    if request.method == 'POST':
        # get new password
        newPassword = request.form.get('password')
        # print(newPassword)

        # get email of current user
        current_user_email = get_jwt_identity()
        # print(current_user_email)

        # find user by email
        user = db.session.query(staff).filter(
            staff.email == current_user_email).first()
        # print(user)

        if user:
            # update the password
            user.set_password(newPassword)

            # commit changes to DB
            db.session.commit()

    return render_template('settings.html')
