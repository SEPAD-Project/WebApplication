from flask import render_template, request, redirect, url_for, Blueprint
from flask_login import current_user, login_required
from app import db
from app.models._class import Class
from app.models.teacher import Teacher
from app.models.student import Student
from app.utils.generate_class_code import generate_class_code


bp = Blueprint('class_routes', __name__)

@bp.route('/panel/classes', methods=['GET', 'POST'])
@login_required
def go_to_panel_classes():
    query = request.args.get('q')
    if query == "" or query is None:
        classes = Class.query.filter(Class.school_code == current_user.school_code).all()
    else:
        classes = Class.query.filter(
            (Class.school_code == current_user.school_code) &
            ((Class.class_name.ilike(f'%{query}%')) |
             (Class.class_code.ilike(f'%{query}%')))
        ).all()

    return render_template('class/classes.html', classes=classes)


@bp.route('/panel/add_class', methods=['GET', 'POST'])
@login_required
def go_to_add_class():
    school_code = current_user.school_code
    teachers = []

    if request.method == 'POST':
        class_name = request.form['class_name']
        class_code = generate_class_code(school_code, class_name)
        try:
            new_class = Class(class_name, class_code, school_code, teachers)
            db.session.add(new_class)
            db.session.commit()
        except:
            return redirect(url_for('class_routes.go_to_duplicated_class_info'))
        
        return redirect(url_for('class_routes.go_to_panel_classes'))

    return render_template('class/add_class.html')


@bp.route('/duplicated_class_info')
@login_required
def go_to_duplicated_class_info():
    return render_template('class/duplicated_class_info.html')

@bp.route('/panel/class_info/<class_name>')
@login_required
def go_to_class_info(class_name):
    school_code = current_user.school_code
    class_code = generate_class_code(school_code, class_name)

    class_ = Class.query.filter(Class.class_code == class_code).first()

    teachers = [Teacher.query.filter(Teacher.teacher_national_code == national_code).first() for national_code in class_.teachers]
    students = Student.query.filter(Student.class_code == class_.class_code).all()

    return render_template('class/class_info.html', data=class_, teachers=teachers, students=students)