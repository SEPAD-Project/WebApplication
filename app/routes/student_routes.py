from flask import render_template, Blueprint, request, redirect, url_for
from flask_login import login_required, current_user
from app.models.student import Student
from app.models._class import Class
from app import db


bp = Blueprint('student_routes', __name__)


@bp.route('/panel/students')
@login_required
def go_to_panel_students():
    query = request.args.get('q')

    if query:
        students = Student.query.filter(
            ((Student.student_name.ilike(f"%{query}%")) |
            (Student.student_family.ilike(f"%{query}%")) |
            (Student.student_national_code.ilike(f"%{query}%"))) &
            
            (Student.school_code == current_user.school_code)
        ).all()
    else:
        students = Student.query.filter(Student.school_code == current_user.school_code).all()
    
    return render_template('student/students.html', students=students)

@bp.route("/panel/students/add_student", methods=['GET', 'POST'])
@login_required
def go_to_add_student():
    if request.method == 'POST':
        student_name = request.form['student_name']
        student_family = request.form['student_family']
        student_national_code = request.form['student_national_code']
        student_password = request.form['student_password']

        class_code = request.form['selected_class']
        school_code= current_user.school_code

        new_student = Student(student_name, student_family, student_national_code, student_password, class_code, school_code)
        db.session.add(new_student)

        try:
            db.session.commit()
        except:
            db.session.rollback()
            return redirect(url_for('student_routes.go_to_duplicated_student_info_add'))

        return redirect(url_for('student_routes.go_to_panel_students'))

    classes = Class.query.filter(Class.school_code == current_user.school_code).all()
    return render_template('student/add_student.html', classes=classes)

@bp.route("/panel/students/student_info/<student_national_code>")
@login_required
def go_to_student_info(student_national_code):
    student = Student.query.filter((Student.student_national_code == student_national_code) & (Student.school_code == current_user.school_code)).first()
    return render_template('student/student_info.html', data=student)

@bp.route("/panel/students/edit_student/<student_national_code>", methods=['GET', 'POST'])
@login_required
def go_to_edit_student(student_national_code):
    if request.method == "POST":
        new_name = request.form['student_name']
        new_family = request.form['student_family']
        new_national_code = request.form['student_national_code']
        new_password = request.form['student_password']
        new_class = request.form['selected_class']

        student = Student.query.filter(Student.student_national_code == student_national_code).first()

        student.student_name = new_name
        student.student_family = new_family
        student.student_national_code = new_national_code
        student.student_password = new_password
        student.class_code = new_class

        try:
            db.session.commit()
        except:
            db.session.rollback()
            return redirect(url_for('student_routes.go_to_duplicated_student_info_edit', student_national_code=student.student_national_code))

        return redirect(url_for('student_routes.go_to_panel_students'))

    classes = Class.query.filter(Class.school_code == current_user.school_code).all()
    student = Student.query.filter((Student.student_national_code == student_national_code) & (Student.school_code == current_user.school_code)).first()
    return render_template('student/edit_student.html', student=student, classes=classes)

@bp.route("/panel/students/duplicated_student_info_add", methods=['GET', 'POST'])
@login_required
def go_to_duplicated_student_info_add():
    return render_template('student/duplicated_student_info_add.html')

@bp.route("/panel/students/duplicated_student_info_edit/<student_national_code>", methods=['GET', 'POST'])
@login_required
def go_to_duplicated_student_info_edit(student_national_code):
    return render_template('student/duplicated_student_info_edit.html', student_national_code=student_national_code)