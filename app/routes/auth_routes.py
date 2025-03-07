from flask import render_template, request, redirect, url_for, Blueprint
from flask_login import login_user, current_user
from app import db
from app.models.school import School

bp = Blueprint('auth_routes', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def go_to_login():
    if current_user.is_authenticated:
        return redirect(url_for('school_routes.go_to_panel_home'))

    if request.method == 'POST':
        given_school_code = request.form['username']
        given_manager_personal_code = request.form['password']

        school = School.query.filter(School.school_code == given_school_code).first()
        if school is None:
            return redirect(url_for('auth_routes.go_to_unknown_school_info'))

        if school.manager_personal_code == given_manager_personal_code:
            login_user(school, remember=True)
            return redirect(url_for('school_routes.go_to_panel_home'))
        else:
            return redirect(url_for('auth_routes.go_to_unknown_school_info'))

    return render_template('auth/login.html')


@bp.route('/signup', methods=['GET', 'POST'])
def go_to_signup():
    if request.method == 'POST':
        school_name = request.form['school_name']
        school_code = request.form['school_code']
        manager_personal_code = request.form['manager_personal_code']
        province = request.form['province']
        city = request.form['city']

        new_school = School(school_name=school_name, 
                            school_code=school_code,
                            manager_personal_code=manager_personal_code,
                            province=province,
                            city=city,
                            teachers="[]")
        
        try:
            db.session.add(new_school)
            db.session.commit()
        except:
            return redirect(url_for('auth_routes.go_to_duplicated_school_info'))
        
        return redirect(url_for('auth_routes.go_to_notify_user'))
    
    return render_template('auth/signup.html')


@bp.route('/notify_username_password')
def go_to_notify_user():
    return render_template('auth/notify_username_password.html')


@bp.route('/duplicated_school_info')
def go_to_duplicated_school_info():
    return render_template('auth/duplicated_school_info.html')


@bp.route('/unknown_school_info')
def go_to_unknown_school_info():
    return render_template('auth/unknown_school_info.html')