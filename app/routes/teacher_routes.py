from flask import render_template, Blueprint
from flask_login import login_required, current_user
from app import db
from app.models._class import Class
from app.models.teacher import Teacher


bp = Blueprint('teacher_routes', __name__)


@bp.route('/panel/teachers')
@login_required
def go_to_panel_teachers():
    school_classes = Class.query.filter(Class.school_code == current_user.school_code).all()
    school_teachers = set({})

    for school_class in school_classes:
        class_teachers = school_class.teachers
        for teacher_national_code in class_teachers:
            teacher = Teacher.query.filter(Teacher.teacher_national_code == teacher_national_code).first()
            school_teachers.add(teacher)

    school_teachers = sorted(school_teachers)
    return render_template('teacher/teachers.html', teachers=school_teachers)