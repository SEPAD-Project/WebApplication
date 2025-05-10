# Standard Library Imports
from random import randint
from pathlib import Path

# Third-party Imports
from flask import Blueprint, redirect, render_template, request, url_for, session
from flask_login import login_user, current_user

# Local Application Imports
from source import db
from source.models.models import School
from source.server_side.Website.directory_manager import dm_create_school
from source.server_side.Website.Email.signup_verify import verify_code_sender

# Initialize the Blueprint for authentication-related routes
bp = Blueprint('auth_routes', __name__)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    '''
    Handle the login process for school managers.

    GET:
        - If the user is already authenticated, redirect to the dashboard.
        - Otherwise, render the login form.

    POST:
        - Retrieve school code and manager's personal code from the form.
        - Authenticate the user against the database.
        - If credentials are valid, log the user in and redirect to the panel home.
        - If invalid, redirect to an error notification page.
    '''
    if current_user.is_authenticated:
        # User is already logged in; redirect to dashboard
        return redirect(url_for('school_routes.panel_home'))

    if request.method == 'POST':
        # Retrieve login form data
        given_school_code = request.form['username']
        given_manager_personal_code = request.form['password']

        # Query the database for a school with the given code
        school = School.query.filter_by(school_code=given_school_code).first()

        if not school:
            # No school found with the provided code
            session['show_error_notif'] = True
            return redirect(url_for('auth_routes.unknown_school_info'))

        if school.manager_personal_code == given_manager_personal_code:
            # Credentials are valid; log the user in
            login_user(school, remember=True)
            return redirect(url_for('school_routes.panel_home'))
        else:
            # Invalid manager personal code
            session['show_error_notif'] = True
            return redirect(url_for('auth_routes.unknown_school_info'))

    # Render login page for GET request
    return render_template('auth/login.html')


@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    '''
    Handle the registration process for new schools.

    GET:
        - Render the signup form.

    POST:
        - Collect school registration data from the form.
        - Create a new school record and save it in the database.
        - Create a directory for the new school.
        - If an error occurs (e.g., duplicate entry), redirect to an error page.
    '''
    if request.method == 'POST':
        generated_code = str(randint(1000000, 9999999))

        # Retrieve registration form data
        session['tmp_school_data'] = {
            'school_name' : request.form['school_name'],
            'school_code' : request.form['school_code'],
            'manager_personal_code' : request.form['manager_personal_code'],
            'province' : request.form['province'],
            'city' : request.form['city'],
            'email' : request.form['email'],
            'generated_code' : generated_code,
            'attempts_count' : 0
        }


        template_path = Path(__file__).parent.parent / 'server_side' / 'Website' / 'Email' / 'templates' / 'signup_verify.html'

        with open(template_path, 'r') as file:
            html_content = file.read().replace('{{ verification_code }}', generated_code)

        verify_code_sender(request.form['email'], 'Verify Email', html_content)

        return redirect(url_for('auth_routes.verify_email'))

    # Render signup page for GET request
    return render_template('auth/signup.html')

@bp.route('/verify_email', methods=['GET', 'POST'])
def verify_email():
    if request.method=="POST":
            temp_data = session.get('tmp_school_data')
            entered_code = request.form['code']

            print(session['tmp_school_data']['attempts_count'])
            if session['tmp_school_data']['attempts_count'] < 3:
                session['tmp_school_data']['attempts_count'] += 1
                session.modified = True
                if entered_code == temp_data['generated_code']:
                    # Create a new School instance
                    new_school = School(
                        school_name=temp_data['school_name'],
                        school_code=temp_data['school_code'],
                        manager_personal_code=temp_data['manager_personal_code'],  
                        province=temp_data['province'],
                        city=temp_data['city'],
                        email=temp_data['email']
                    )

                    session.pop('tmp_school_data')

                    try:
                        # Add and commit the new school to the database
                        db.session.add(new_school)
                        db.session.commit()

                        # Create a corresponding directory for the school
                        dm_create_school(school_id=str(new_school.id))

                        # Notify user of successful registration
                        session['show_error_notif'] = True
                        return redirect(url_for('auth_routes.notify_user'))

                    except Exception:
                        # Error occurred (e.g., duplicate school code)
                        session['show_error_notif'] = True
                        return redirect(url_for('auth_routes.duplicated_school_info'))
            else:
                session.pop('tmp_school_data')
                return redirect(url_for('auth_routes.signup'))

    return render_template("auth/verify_email.html")


@bp.route('/notify_username_password')
def notify_user():
    """
    Display a page that informs the user of their assigned username and password after registration.

    Prevents direct access without proper session context by checking the session flag.
    """
    # Check session flag to prevent unauthorized access
    if not session.pop('show_error_notif', False):
        return redirect(url_for('auth_routes.login'))

    # Render notification page
    return render_template('auth/notify_username_password.html')


@bp.route('/duplicated_school_info')
def duplicated_school_info():
    """
    Show an error page when a duplicate school code or personal code is detected during signup.

    Prevents direct access without proper session context by checking the session flag.
    """
    # Check session flag to prevent unauthorized access
    if not session.pop('show_error_notif', False):
        return redirect(url_for('auth_routes.signup'))

    # Render duplicate information error page
    return render_template('auth/duplicated_school_info.html')


@bp.route('/unknown_school_info')
def unknown_school_info():
    """
    Display an error message when the provided school code does not exist
    or the manager personal code is incorrect.

    Prevents direct access without proper session context by checking the session flag.
    """
    # Check session flag to prevent unauthorized access
    if not session.pop('show_error_notif', False):
        return redirect(url_for('auth_routes.signup'))

    # Render unknown school information error page
    return render_template('auth/unknown_school_info.html')
