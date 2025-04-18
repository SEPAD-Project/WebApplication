# Import necessary modules
from app import db  # SQLAlchemy database instance
from app.models.models import School  # School model for database interaction
# Function to manage school directories
from app.server_side.Website.directory_manager import dm_create_school

# Flask web utilities
from flask import Blueprint, redirect, render_template, request, url_for, session
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
    # Redirect authenticated users to the dashboard
    if current_user.is_authenticated:
        return redirect(url_for('school_routes.panel_home'))

    if request.method == 'POST':
        # Retrieve login credentials from the form
        given_school_code = request.form['username']
        given_manager_personal_code = request.form['password']

        # Query the database for the school
        school = School.query.filter_by(school_code=given_school_code).first()

        if not school:
            # School code not found
            session["show_error_notif"] = True
            return redirect(url_for('auth_routes.unknown_school_info'))

        # Validate the manager's personal code
        if school.manager_personal_code == given_manager_personal_code:
            login_user(school, remember=True)
            return redirect(url_for('school_routes.panel_home'))
        else:
            # Invalid personal code
            session["show_error_notif"] = True
            return redirect(url_for('auth_routes.unknown_school_info'))

    # Render the login page for GET requests
    return render_template('auth/login.html')


@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    Handles the registration process for new schools.

    GET:
        - Renders the signup form.

    POST:
        - Collects data from the form and creates a new School record.
        - Attempts to commit it to the database.
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
            # Add the new school to the database
            db.session.add(new_school)
            db.session.commit()

            # Create a directory for the school
            dm_create_school(school_code=school_code)

            # Notify the user of successful registration
            session["show_error_notif"] = True
            return redirect(url_for('auth_routes.notify_user'))
        except Exception as e:
            # Handle database errors (e.g., duplicate entries)
            session["show_error_notif"] = True
            return redirect(url_for('auth_routes.duplicated_school_info'))

    # Render the signup form for GET requests
    return render_template('auth/signup.html')


@bp.route('/notify_username_password')
def notify_user():
    """
    Displays a page that informs the user of their assigned username and password after registration.

    Prevents direct access without context by checking the session flag.
    """
    if not session.pop('show_error_notif', False):
        return redirect(url_for('auth_routes.login'))
    return render_template('auth/notify_username_password.html')


@bp.route('/duplicated_school_info')
def duplicated_school_info():
    """
    Shows an error page when a school code or personal code already exists during signup.

    Prevents direct access without context by checking the session flag.
    """
    if not session.pop('show_error_notif', False):
        return redirect(url_for('auth_routes.signup'))
    return render_template('auth/duplicated_school_info.html')


@bp.route('/unknown_school_info')
def unknown_school_info():
    """
    Displays an error message when:
    - The provided school code does not exist, or
    - The manager personal code (password) is incorrect.

    Prevents direct access without context by checking the session flag.
    """
    if not session.pop('show_error_notif', False):
        return redirect(url_for('auth_routes.signup'))
    return render_template('auth/unknown_school_info.html')
