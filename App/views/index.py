from flask import Blueprint, request, jsonify, render_template
from App.database import db
from App.models import Staff, Course, Assessment, Programme, Admin, Semester, CourseStaff
from App.models.staff import Role
from App.models.assessment import ApprovalStatus
from datetime import datetime

index_views = Blueprint('index_views', __name__,
                        template_folder='../templates')

# Gets Landing Page


@index_views.route('/', methods=['GET'])
def index():
    return render_template('startPage.html')

@index_views.route('/login', methods=['GET'])
def login():
   return render_template('login.html')

@index_views.route('/signup', methods=['GET'])
def signup():
   return render_template('signup.html')

@index_views.route('/init', methods=['GET'])
def init():
    db.drop_all()
    db.create_all()

    # create admin
   #  bob = Admin(u_ID=999, email="bob@gmail.com", password="bobpass")
    bob = Admin(u_ID=999, public_ID="unique_id_value", email="bob@gmail.com", password="bobpass")
    db.session.add(bob)

    # create semester
    sem = Semester(start_date=datetime.strptime('01-02-2024', '%d-%m-%Y').date(),
                   end_date=datetime.strptime('01-05-2024', '%d-%m-%Y').date(),
                   semester_number=1, weekly_assessment_limit=3)

    db.session.add(sem)

    # create courses
   #  c1 = Course(courseCode='COMP1700', courseTitle='Introduction to C++',
   #              description='C++ basics', level=1, semester=1, aNum=3)

    c1 = Course(id=480, code='COMP1700', name='Introduction to C++', description='C++ basics', credits='3', level=1)

   #  c1 = Course.addCourse(code='COMP1700', name='Introduction to C++', description='C++ basics', credits='3', level=1)

    c2 = Course(id=481, code='COMP1701', name='Introduction to Web Development',
                description='Web development basics', credits='3', level=1)

    c3 = Course(id=482, code='COMP2700', name='Advanced C++',
                description='Advanced C++',  credits='3',level=2)
    c4 = Course(id=483, code='COMP2701', name='Advanced Web Development',
                description='Advanced web development',  credits='3',level=2)
    c5 = Course(id=484, code='COMP3700', name='Data Science Fundamentals',
                description='Introduction to python and datasets',  credits='3',level=3)
    c6 = Course(id=485, code='COMP3701', name='Advanced Data Science',
                description='Analyzing Big Data with Python',  credits='3',level=3)
    db.session.add(c1)
    db.session.add(c2)
    db.session.add(c3)
    db.session.add(c4)
    db.session.add(c5)
    db.session.add(c6)

    # create staff
   #  fix problem with id
    staff = Staff.register(first_name='Jane', last_name='Doe', id=984, public_ID= 984,
                           global_role=Role.INSTRUCTOR, email='jane@mail.com', password='password')

    # assign staff to courses
    cs1 = CourseStaff(staff_id= 984, course_offering_id=1 , course_role= 'test1', start_date=datetime.strptime('04-08-2024', '%d-%m-%Y').date(),
                           end_date=datetime.strptime('04-08-2024', '%d-%m-%Y').date())
                           
    cs2 = CourseStaff(staff_id= 984, course_offering_id=2 , course_role= 'test2', start_date=datetime.strptime('04-08-2024', '%d-%m-%Y').date(),
                           end_date=datetime.strptime('04-08-2024', '%d-%m-%Y').date())

    cs3 = CourseStaff(staff_id= 984, course_offering_id=3 , course_role= 'test3', start_date=datetime.strptime('04-08-2024', '%d-%m-%Y').date(),
                           end_date=datetime.strptime('04-08-2024', '%d-%m-%Y').date())
    db.session.add(cs1)
    db.session.add(cs2)
    db.session.add(cs3)

    # create assessments
   #  asm1 = Assessment(category='EXAM')
   #  db.session.add(asm1)
   #  asm2 = Assessment(category='ASSIGNMENT')
   #  db.session.add(asm2)
   #  asm3 = Assessment(category='QUIZ')
   #  db.session.add(asm3)
   #  asm4 = Assessment(category='PROJECT')
   #  db.session.add(asm4)
   #  asm5 = Assessment(category='DEBATE')
   #  db.session.add(asm5)
   #  asm6 = Assessment(category='PRESENTATION')
   #  db.session.add(asm6)
   #  asm7 = Assessment(category='ORALEXAM')
   #  db.session.add(asm7)
   #  asm8 = Assessment(category='PARTICIPATION')
   #  db.session.add(asm8)

    # create course assessments

   # def __init__(self, course_offering_id: int, category_id: int, name: str, status: ApprovalStatus,
   #               start_date, end_date, start_time, end_time, weight: float)

    ca1 = Assessment(course_offering_id=1,category_id=1, name='Assessment1',status=ApprovalStatus.APPROVED,
                           start_date=datetime.strptime('04-08-2024', '%d-%m-%Y').date(),
                           end_date=datetime.strptime('04-08-2024', '%d-%m-%Y').date(),
                           start_time=datetime.strptime('08:00:00', '%H:%M:%S').time(),
                           end_time=datetime.strptime('10:00:00', '%H:%M:%S').time(), weight=0.2)

    ca2 = Assessment(course_offering_id=2,category_id=1, name='Assessment2', status=ApprovalStatus.APPROVED, 
                           start_date=datetime.strptime('04-08-2024', '%d-%m-%Y').date(),
                           end_date=datetime.strptime('04-09-2024', '%d-%m-%Y').date(),
                           start_time=datetime.strptime('08:00:00', '%H:%M:%S').time(),
                           end_time=datetime.strptime('10:00:00', '%H:%M:%S').time(), weight=0.2)

    ca3 = Assessment(course_offering_id=3,category_id=1, name='Assessment3', status=ApprovalStatus.APPROVED,
                           start_date=datetime.strptime('04-08-2024', '%d-%m-%Y').date(),
                           end_date=datetime.strptime('04-10-2024', '%d-%m-%Y').date(),
                           start_time=datetime.strptime('08:00:00', '%H:%M:%S').time(),
                           end_time=datetime.strptime('10:00:00', '%H:%M:%S').time(), weight=0.2)

    db.session.add(ca1)
    db.session.add(ca2)
    db.session.add(ca3)


    db.session.commit()
    return {'message': 'Objects created'}
