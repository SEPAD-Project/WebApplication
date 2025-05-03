# Third-party Imports
from flask import Blueprint, render_template
from flask_login import current_user, login_required

# Local Application Imports
from app.models.models import School

# Initialize the Blueprint for school-related routes
bp = Blueprint('school_routes', __name__)


@bp.route('/panel/home')
@login_required
def panel_home():
    """
    Render the dashboard (home page) for authenticated school users.

    Returns:
        Rendered HTML template for the school panel's home page.
    """
    return render_template('school/home.html')


@bp.route('/panel/school_info')
@login_required
def panel_school_info():
    """
    Display detailed information about the current school.

    Retrieves the school based on the currently logged-in user.
    Gathers and sends statistics (teachers, classes, students) to the template.

    Returns:
        Rendered HTML template with school details and counts.
    """
    # Retrieve the school by the current user's ID
    school = School.query.filter(School.id == current_user.id).first()

    if not school:
        # If the school is not found, return a 404 page
        return render_template('errors/404.html'), 404

    # Gather stats
    teachers_count = len(school.teachers)
    classes_count = len(school.classes)
    students_count = len(school.students)

    return render_template(
        'school/school_info.html',
        data=school,
        tc=teachers_count,
        cc=classes_count,
        sc=students_count
    )
