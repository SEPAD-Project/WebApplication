from flask import render_template, request, redirect, url_for, Blueprint
from flask_login import current_user, login_required
from app import db
from app.models._class import Class
from app.utils.generate_class_code import generate_class_code


bp = Blueprint('class_routes', __name__)

@bp.route('/panel/classes', methods=['GET', 'POST'])
@login_required
def go_to_panel_classes():
    classes = Class.query.filter(Class.school_code == int(current_user.school_code)).all()
    return render_template('class/classes.html', classes=classes)


@bp.route('/add_class', methods=['GET', 'POST'])
@login_required
def go_to_add_class():
    school_code = int(current_user.school_code)
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