from flask import render_template, Blueprint, request, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models._class import Class
from app.models.teacher import Teacher
from app.models.school import School
from app.utils.generate_class_code import generate_class_code


bp = Blueprint('teacher_routes', __name__)


@bp.route('/panel/teachers')
@login_required
def go_to_panel_teachers():
    school = School.query.filter(School.school_code == current_user.school_code).first()
    teachers = []
    for national_code in eval(school.teachers):
        teachers.append(Teacher.query.filter(Teacher.teacher_national_code == national_code).first())
        
    query = request.args.get('q')
    if query:
        filtered_teachers = []
        for teacher in teachers:
            if (query.lower() in teacher.teacher_name.lower() or query.lower() in teacher.teacher_national_code.lower()):
                filtered_teachers.append(teacher)
        teachers = filtered_teachers

    return render_template('teacher/teachers.html', teachers=teachers)

@bp.route('/panel/teachers/add_teacher', methods=['GET', 'POST'])
@login_required
def go_to_add_teacher():
    if request.method == 'POST':
        entry_national_code = request.form["teacher_national_code"]
        entry_password = request.form["teacher_password"]
        teacher = Teacher.query.filter(Teacher.teacher_national_code == entry_national_code).first()
        if teacher is None:
            return redirect(url_for("teacher_routes.go_to_wrong_teacher_info"))
        if teacher.teacher_password == entry_password:
            classes = request.form.getlist("selected_classes")
            if classes:
                school = School.query.filter(School.school_code == current_user.school_code).first()
                teachers = eval(school.teachers)
                teachers.append(teacher.teacher_national_code)
                school.teachers = str(teachers)
                db.session.commit()
            for class_code in classes:
                teacher_classes = eval(teacher.teacher_classes)
                teacher_classes.append(class_code)
                teacher.teacher_classes = str(teacher_classes)

                class_ = Class.query.filter(Class.class_code == class_code).first()
                class_teachers = eval(class_.teachers)
                class_teachers.append(entry_national_code)
                class_.teachers = str(class_teachers)

                db.session.commit()
            return redirect(url_for("teacher_routes.go_to_add_teacher"))
        else:
            return redirect(url_for("teacher_routes.go_to_wrong_teacher_info"))
        
    school_classes = Class.query.filter(Class.school_code == current_user.school_code).all()
    print([class_.class_code for class_ in school_classes])
    return render_template("teacher/add_teacher.html", classes = school_classes)

@bp.route("/panel/students/remove_teacher/<teacher_national_code>", methods=['POST', 'GET'])
@login_required
def go_to_remove_teacher(teacher_national_code):
    teacher = Teacher.query.filter(Teacher.teacher_national_code == teacher_national_code).first()
    school_code = generate_class_code(current_user.school_code, '')
    teacher_classes = eval(teacher.teacher_classes)
    for class_ in teacher_classes:
        if class_[:3] == school_code:
            teacher_classes.remove(class_)
    teacher.teacher_classes = str(teacher_classes)

    classes = Class.query.filter(Class.school_code == current_user.school_code).all()
    for class_ in classes:
        teachers = eval(class_.teachers)
        try:
            teachers.remove(teacher_national_code)
        except:
            continue
        class_.teachers = str(teachers)

    school = School.query.filter(School.school_code == current_user.school_code).first()
    school_teachers = eval(school.teachers)
    school_teachers.remove(teacher_national_code)
    school.teachers = str(school_teachers)

    db.session.commit()
    return redirect(url_for('teacher_routes.go_to_panel_teachers'))

@bp.route('/panel/wrong_teacher_info', methods=['GET', 'POST'])
@login_required
def go_to_wrong_teacher_info():
    return render_template("teacher/wrong_teacher_info.html")

@bp.route("/panel/teachers/teacher_info/<teacher_national_code>")
@login_required
def go_to_teacher_info(teacher_national_code):
    school = School.query.filter((School.school_code == current_user.school_code)).first()
    teacher = Teacher.query.filter((Teacher.teacher_national_code == teacher_national_code)).first()
    if teacher.teacher_national_code in eval(school.teachers):
         return render_template('teacher/teacher_info.html', data=teacher)