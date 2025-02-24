from flask import render_template, Blueprint, request
from flask_login import login_required, current_user
from app import db
from app.models._class import Class
from app.models.teacher import Teacher


bp = Blueprint('teacher_routes', __name__)


@bp.route('/panel/teachers')
@login_required
def go_to_panel_teachers():
    query = request.args.get('q')

    if query == "" or query is None:
        school_classes = Class.query.filter(Class.school_code == current_user.school_code).all()
        school_teachers = set()

        for school_class in school_classes:
            class_teachers = school_class.teachers
            for teacher_national_code in class_teachers:
                teacher = Teacher.query.filter(Teacher.teacher_national_code == teacher_national_code).first()
                if teacher:
                    school_teachers.add(teacher)


        school_teachers = sorted(school_teachers, key=lambda x: (x.teacher_name, x.teacher_family))
        return render_template('teacher/teachers.html', teachers=school_teachers)
    
    else:
        school_classes = Class.query.filter(Class.school_code == current_user.school_code).all()
        school_teachers = set()

        for school_class in school_classes:
            class_teachers = school_class.teachers
            for teacher_national_code in class_teachers:
                teacher = Teacher.query.filter(
                    (Teacher.teacher_national_code == teacher_national_code) &
                    (
                        (Teacher.teacher_name.ilike(f'%{query}%')) |
                        (Teacher.teacher_family.ilike(f'%{query}%')) |
                        (Teacher.teacher_national_code.ilike(f'%{query}%')) 
                    )
                ).first()
                if teacher:
                    school_teachers.add(teacher)

        school_teachers = sorted(school_teachers, key=lambda x: (x.teacher_name, x.teacher_family))
        return render_template('teacher/teachers.html', teachers=school_teachers)

@bp.route('/panel/add_teacher')
@login_required
def go_to_add_teacher():
    return render_template("teacher/add_teacher.html")