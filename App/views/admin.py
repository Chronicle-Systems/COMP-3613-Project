from App.controllers import courseAssessment
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_jwt_extended import jwt_required
from App.controllers import Course
from App.models import Admin
from App.database import db
from werkzeug.utils import secure_filename
import os
import csv
from datetime import datetime

from App.controllers.course import (
    add_course,
    list_courses,
    get_course,
    delete_course
)

from App.controllers.semester import (
    create_semester
)

from App.controllers.courseAssessment import (
    get_clashes,
    get_course_assessment_by_id
)

admin_views = Blueprint('admin_views', __name__, template_folder='../templates')

@admin_views.route('/semester', methods=['GET'])
@jwt_required(Admin)
def get_upload_page():
    return render_template('dashboard.html')

@admin_views.route('/uploadFiles', methods=['GET'])
@jwt_required(Admin)
def get_uploadFiles_page():
    return render_template('uploadFiles.html')

@admin_views.route('/coursesList', methods=['GET'])
@jwt_required(Admin)
def index():
    return render_template('courses.html')

@admin_views.route('/newSemester', methods=['POST'])
@jwt_required(Admin)
def new_semester_action():
    if request.method == 'POST':
        semBegins = request.form.get('teachingBegins')
        semEnds = request.form.get('teachingEnds')
        semChoice = request.form.get('semester')
        maxAssessments = request.form.get('maxAssessments')
        start_date = datetime.strptime(semBegins, '%Y-%m-%d') 
        end_date = datetime.strptime(semEnds, '%Y-%m-%d')
        
        try:
            create_semester(start_date, end_date, int(semChoice), int(maxAssessments))
            flash('Semester created successfully')
            return render_template('uploadFiles.html')
        except Exception as e:
            flash(f'Error creating semester: {str(e)}')
            return render_template('semester.html')

@admin_views.route('/uploadcourse', methods=['POST'])
@jwt_required(Admin)
def upload_course_file():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename == '':
            message = 'No file selected!'
            return render_template('uploadFiles.html', message=message)
        else:
            filename = secure_filename(file.filename)
            file.save(os.path.join('App/uploads', filename))
            fpath = 'App/uploads/' + filename
            with open(fpath, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    course = add_course(
                        courseCode=row['Course Code'],
                        courseTitle=row['Course Title'],
                        description=row['Course Description'],
                        level=int(row['Level']),
                        semester=int(row['Semester']),
                        aNum=int(row['Assessment No.'])
                    )
            return redirect(url_for('admin_views.get_courses'))

@admin_views.route('/get_courses', methods=['GET'])
@jwt_required(Admin)
def get_courses():
    courses = list_courses()
    return render_template('courses.html', courses=courses)

@admin_views.route('/newCourse', methods=['GET'])
@jwt_required(Admin)
def get_new_course():
    return render_template('addCourse.html')

@admin_views.route('/addNewCourse', methods=['POST'])
@jwt_required(Admin)
def add_course_action():
    if request.method == 'POST':
        courseCode = request.form.get('course_code')
        title = request.form.get('title')
        description = request.form.get('description')
        level = request.form.get('level')
        semester = request.form.get('semester')
        numAssessments = request.form.get('numAssessments')

        course = add_course(courseCode, title, description, level, semester, numAssessments)
        return redirect(url_for('admin_views.get_courses'))


@admin_views.route('/modifyCourse/<string:courseCode>', methods=['GET'])
@jwt_required(Admin)
def get_update_course(courseCode):
    course = get_course(courseCode) 
    return render_template('updateCourse.html', course=course)


@admin_views.route('/updateCourse', methods=['POST'])
@jwt_required(Admin)
def update_course():
    if request.method == 'POST':
        courseCode = request.form.get('code')
        title = request.form.get('title')
        description = request.form.get('description')
        level = request.form.get('level')
        semester = request.form.get('semester')
        numAssessments = request.form.get('assessment')

        delete_course(get_course(courseCode))
        add_course(courseCode, title, description, level, semester, numAssessments)
        flash("Course Updated Successfully!")
        return redirect(url_for('admin_views.get_courses'))

@admin_views.route("/deleteCourse/<string:courseCode>", methods=["POST"])
@jwt_required(Admin)
def delete_course_action(courseCode):
    if request.method == 'POST':
        course = get_course(courseCode) 
        delete_course(course)
        print(courseCode, " deleted")
        flash("Course Deleted Successfully!")
    return redirect(url_for('admin_views.get_courses'))

@admin_views.route("/clashes", methods=["GET"])
@jwt_required(Admin)
def get_clashes_page():
    all_assessments = courseAssessment.list_assessments()
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    searchResults = []
    if start_date and end_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        for a in all_assessments:
            if start_date <= a.startDate <= end_date or start_date <= a.endDate <= end_date:
                searchResults.append(a)
    assessments = get_clashes()
    return render_template('clashes.html', assessments=assessments, results=searchResults)

@admin_views.route("/acceptOverride/<int:aID>", methods=['POST'])
@jwt_required(Admin)
def accept_override(aID):
    ca = get_course_assessment_by_id(aID)
    if ca:
        ca.clashDetected = False
        db.session.commit()
        print("Accepted override.")
    return redirect(url_for('admin_views.get_clashes_page'))

@admin_views.route("/rejectOverride/<int:aID>", methods=['POST'])
@jwt_required(Admin)
def reject_override(aID):
    ca = get_course_assessment_by_id(aID)
    if ca:
        ca.clashDetected = False
        ca.startDate = None
        ca.endDate = None
        ca.startTime = None
        ca.endTime = None
        db.session.commit()
        print("Rejected override.")
    return redirect(url_for('admin_views.get_clashes_page'))

@admin_views.route('/dashboard')
@jwt_required()
def dashboard():
    return render_template('dashboard.html')

@admin_views.route('/newCourse')
@jwt_required()
def get_new_course_general():
    return render_template('new_course.html')

@admin_views.route('/coursesList')
@jwt_required()
def get_courses_general():
    return render_template('courses.html')

@admin_views.route('/assessments')
@jwt_required()
def get_assessments():
    return render_template('assessments.html')

@admin_views.route('/semester')
@jwt_required()
def get_semester():
    return render_template('semester.html')
