# Import necessary modules
from app.models._class import Class
from app.models.school import School
from app.models.student import Student

from flask import Blueprint, render_template
from flask_login import current_user, login_required

# Initialize the Blueprint for school-related routes
bp = Blueprint('school_routes', __name__)


@bp.route('/panel/home')
@login_required
def panel_home():
    """
    Displays the home page of the school panel.
    """
    return render_template('school/home.html')


@bp.route('/panel/school_info')
@login_required
def panel_school_info():
    """
    Handles the school information section in the panel.
    - Retrieves and displays details about the school, including teacher, class, and student counts.
    """
    # Retrieve the school object from the database using the current user's school code
    school = School.query.filter(School.school_code == current_user.school_code).first()

    # Calculate the number of teachers, classes, and students associated with the school
    teachers_count = len(eval(school.teachers)) if school.teachers else 0
    classes_count = Class.query.filter(Class.school_code == school.school_code).count()
    students_count = Student.query.filter(Student.school_code == school.school_code).count()

    # Render the school info page with the retrieved data
    return render_template(
        'school/school_info.html',
        data=school,
        tc=teachers_count,
        cc=classes_count,
        sc=students_count
    )