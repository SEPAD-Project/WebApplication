from flask import render_template, Blueprint, request
from flask_login import login_required, current_user
from app import db
from app.models._class import Class
from app.models.teacher import Teacher
from app.utils.generate_class_code import generate_class_code
from ast import literal_eval


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

@bp.route('/panel/add_teacher', methods=['GET', 'POST'])
@login_required
def go_to_add_teacher():
    if request.method == 'POST':
        entry_national_code = request.form["teacher_national_code"]
        entry_password = request.form["teacher_password"]
        teacher = Teacher.query.filter(Teacher.teacher_national_code == entry_national_code).first()
        if teacher.teacher_password == entry_password:
            classes = request.form.getlist("selected_classes")
            for class_code in classes:
                teacher_classes = eval(teacher.teacher_classes)
                teacher_classes.append(class_code)
                teacher.teacher_classes = str(teacher_classes)

                class_ = Class.query.filter(Class.class_code == class_code).first()
                class_teachers = eval(class_.teachers)
                class_teachers.append(entry_national_code)
                class_.teachers = str(class_teachers)

                db.session.commit()
        else:
            return "false"
        
    school_classes = Class.query.filter(Class.school_code == current_user.school_code).all()
    print([class_.class_code for class_ in school_classes])
    return render_template("teacher/add_teacher.html", classes = school_classes)