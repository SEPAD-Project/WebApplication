from flask import render_template, Blueprint
from flask_login import login_required, current_user
from app import db
from app.models._class import Class
from app.models.student import Student
from app.models.school import School


bp = Blueprint('school_routes', __name__)


@bp.route('/panel/home')
@login_required
def go_to_panel_home():
    return render_template('school/home.html')


@bp.route('/panel/school_info')
@login_required
def go_to_panel_school_info():
    school = School.query.filter(School.school_code == current_user.school_code).first()
    
    teachers_count = len(eval(school.teachers))
    classes_count = Class.query.filter(Class.school_code == school.school_code).count()
    students_count = Student.query.filter(Student.school_code == school.school_code).count()

    return render_template('school/school_info.html', data=school, tc = teachers_count, cc=classes_count, sc=students_count)