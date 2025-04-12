# Import necessary models from the application
from app.models._class import Class      # Represents classes in a school
from app.models.school import School     # Represents a school
from app.models.student import Student   # Represents students

# Import required Flask modules
from flask import Blueprint, render_template
from flask_login import current_user, login_required

# Initialize the Blueprint for school-related routes
# This Blueprint manages routes related to school information and panel home
bp = Blueprint('school_routes', __name__)


@bp.route('/panel/home')
@login_required  # Ensures only logged-in users can access the panel
def panel_home():
    """
    Displays the home page of the school panel.

    This page serves as a dashboard or welcome screen for authenticated users (e.g., school admins).
    It typically includes an overview or quick access to different parts of the system.
    """
    return render_template('school/home.html')


@bp.route('/panel/school_info')
@login_required  # Access is restricted to authenticated users
def panel_school_info():
    """
    Displays detailed information about the school on the school panel.

    This view:
    - Retrieves the school object using the school code of the currently logged-in user.
    - Calculates and displays:
        - Total number of teachers registered in the school.
        - Total number of classes in the school.
        - Total number of students enrolled in the school.
    - Passes this data to the 'school_info.html' template for rendering.
    """
    # Retrieve the school based on the current user's associated school code
    school = School.query.filter(School.school_code == current_user.school_code).first()

    # Count the number of teachers by evaluating the stored list (as a string)
    teachers_count = len(eval(school.teachers)) if school.teachers else 0

    # Count the number of classes associated with the school
    classes_count = Class.query.filter(Class.school_code == school.school_code).count()

    # Count the number of students enrolled in the school
    students_count = Student.query.filter(Student.school_code == school.school_code).count()

    # Render the school_info.html template with all calculated data
    return render_template(
        'school/school_info.html',
        data=school,           # The full school object
        tc=teachers_count,     # Teacher count
        cc=classes_count,      # Class count
        sc=students_count      # Student count
    )

@bp.route('/panel/analytics')
@login_required
def analytics_menu():
    return render_template("school/analytics.html")