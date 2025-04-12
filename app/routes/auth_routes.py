# Import necessary modules
from app import db  # SQLAlchemy database instance
from app.models.school import School  # School model for database interaction
from app.server_side.Website.directory_manager import dm_create_school  # Function to manage school directories

from flask import Blueprint, redirect, render_template, request, url_for, session  # Flask web utilities
from flask_login import login_user, current_user  # User session management

# Initialize the Blueprint for authentication-related routes
bp = Blueprint('auth_routes', __name__)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handles the login process for a school manager.

    GET:
        - If the user is already authenticated, redirect them to the dashboard.
        - Otherwise, show the login form.

    POST:
        - Extracts the provided school code and manager personal code from the form.
        - Authenticates against the database.
        - If valid, logs in the user and redirects to the panel home.
        - Otherwise, redirects to an error notification page.
    """
    # If the user is already logged in, redirect to the panel
    if current_user.is_authenticated:
        return redirect(url_for('school_routes.panel_home'))

    if request.method == 'POST':
        # Retrieve login form data
        given_school_code = request.form['username']
        given_manager_personal_code = request.form['password']

        # Attempt to find the school using the provided code
        school = School.query.filter(School.school_code == given_school_code).first()

        if school is None:
            # School not found
            session["show_error_notif"] = True
            return redirect(url_for('auth_routes.unknown_school_info'))

        # Check if the password matches
        if school.manager_personal_code == given_manager_personal_code:
            login_user(school, remember=True)
            return redirect(url_for('school_routes.panel_home'))
        else:
            # Incorrect password
            session["show_error_notif"] = True
            return redirect(url_for('auth_routes.unknown_school_info'))

    # Show login page for GET request
    return render_template('auth/login.html')


@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    Handles the registration process for new schools.

    GET:
        - Renders the signup form.

    POST:
        - Collects data from the form and creates a new School record.
        - Tries to commit it to the database.
        - If successful, also creates a corresponding directory for the school.
        - If there's a conflict (e.g., duplicate school code), redirects to an error page.
    """
    if request.method == 'POST':
        # Collect registration data from the form
        school_name = request.form['school_name']
        school_code = request.form['school_code']
        manager_personal_code = request.form['manager_personal_code']
        province = request.form['province']
        city = request.form['city']
        email = request.form['email']

        # Create a new School object
        new_school = School(
            school_name=school_name,
            school_code=school_code,
            manager_personal_code=manager_personal_code,
            province=province,
            city=city,
            teachers="[]",  # Initialize empty list of teachers
            email=email
        )

        try:
            # Attempt to add to the database
            db.session.add(new_school)
            db.session.commit()

            # Create a directory for this school
            dm_create_school(school_code=school_code)
        except:
            # Likely a duplicate entry or DB error
            session["show_error_notif"] = True
            return redirect(url_for('auth_routes.duplicated_school_info'))

        # Inform the user of successful registration
        session["show_error_notif"] = True
        return redirect(url_for('auth_routes.notify_user'))

    # Render signup form
    return render_template('auth/signup.html')


@bp.route('/notify_username_password')
def notify_user():
    """
    Displays a page that informs the user of their assigned username and password after registration.

    If accessed without context (e.g., direct visit), it redirects to the login page.
    """
    if not session.get('show_error_notif', False):
        return redirect(url_for('auth_routes.login'))
    session.pop('show_error_notif', None)
    return render_template('auth/notify_username_password.html')


@bp.route('/duplicated_school_info')
def duplicated_school_info():
    """
    Shows an error page when a school code or personal code already exists during signup.

    Prevents direct access without context.
    """
    if not session.get('show_error_notif', False):
        return redirect(url_for('auth_routes.signup'))
    session.pop('show_error_notif', None)
    return render_template('auth/duplicated_school_info.html')


@bp.route('/unknown_school_info')
def unknown_school_info():
    """
    Displays an error message when:
    - The provided school code does not exist, or
    - The manager personal code (password) is incorrect.

    Prevents direct access without context.
    """
    if not session.get('show_error_notif', False):
        return redirect(url_for('auth_routes.signup'))
    session.pop('show_error_notif', None)
    return render_template('auth/unknown_school_info.html')
