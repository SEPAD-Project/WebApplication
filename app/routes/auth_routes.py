# Import necessary modules
from app import db
from app.models.school import School
from app.server_side.directory_manager import create_school

from flask import Blueprint, redirect, render_template, request, url_for, session
from flask_login import login_user, current_user

# Initialize the Blueprint for authentication routes
bp = Blueprint('auth_routes', __name__)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handles user login process.
    - If the user is already authenticated, redirects to the panel home.
    - For POST requests, validates the provided credentials and logs the user in if valid.
    - For GET requests, renders the login form.
    """
    # Redirect to the panel home if the user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('school_routes.panel_home'))

    # Handle POST request: Process login form data
    if request.method == 'POST':
        # Retrieve form data
        given_school_code = request.form['username']
        given_manager_personal_code = request.form['password']

        # Query the database to find the school by school code
        school = School.query.filter(School.school_code == given_school_code).first()

        # Redirect to an error page if the school is not found in the database
        if school is None:
            session["show_error_notif"] = True
            return redirect(url_for('auth_routes.unknown_school_info'))

        # Validate the manager's personal code (password)
        if school.manager_personal_code == given_manager_personal_code:
            # Log the user in using Flask-Login and remember the session
            login_user(school, remember=True)
            return redirect(url_for('school_routes.panel_home'))
        else:
            # Redirect to an error page if the password is incorrect
            session["show_error_notif"] = True
            return redirect(url_for('auth_routes.unknown_school_info'))

    # Handle GET request: Render the login form
    return render_template('auth/login.html')


@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    Handles user registration process.
    - For POST requests, collects form data, creates a new school record, and adds it to the database.
    - For GET requests, renders the signup form.
    """
    # Handle POST request: Process signup form data
    if request.method == 'POST':
        # Retrieve form data
        school_name = request.form['school_name']
        school_code = request.form['school_code']
        manager_personal_code = request.form['manager_personal_code']
        province = request.form['province']
        city = request.form['city']

        # Create a new School object with the collected data
        new_school = School(
            school_name=school_name,
            school_code=school_code,
            manager_personal_code=manager_personal_code,
            province=province,
            city=city,
            teachers="[]"
        )

        try:
            # Add the new school record to the database
            db.session.add(new_school)
            db.session.commit()
            create_school(school_code=school_code)
        except:
            # Redirect to an error page if the school code or manager personal code is already registered
            session["show_error_notif"] = True
            return redirect(url_for('auth_routes.duplicated_school_info'))

        # Notify the user of their username and password
        session["show_error_notif"] = True
        return redirect(url_for('auth_routes.notify_user'))

    # Handle GET request: Render the signup form
    return render_template('auth/signup.html')


@bp.route('/notify_username_password')
def notify_user():
    """
    Displays a page to notify the user of their username and password after registration.
    """
    if not session.get('show_error_notif', False):
        return redirect(url_for('auth_routes.login'))
    session.pop('show_error_notif', None)
    return render_template('auth/notify_username_password.html')


@bp.route('/duplicated_school_info')
def duplicated_school_info():
    """
    Displays an error page when a duplicate school code or manager personal code is detected during registration.
    """
    if not session.get('show_error_notif', False):
        return redirect(url_for('auth_routes.signup'))
    session.pop('show_error_notif', None)
    return render_template('auth/duplicated_school_info.html')


@bp.route('/unknown_school_info')
def unknown_school_info():
    """
    Displays an error page when an unknown school code or incorrect password is provided during login.
    """
    if not session.get('show_error_notif', False):
        return redirect(url_for('auth_routes.signup'))
    session.pop('show_error_notif', None)
    return render_template('auth/unknown_school_info.html')