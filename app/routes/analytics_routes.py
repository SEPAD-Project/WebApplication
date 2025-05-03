# Flask imports
from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import login_required, current_user
from threading import Thread

# Analytics logic
from app.utils.analytics.Generator.analytics_Generator import (
    calculate_students_accuracy,
    calculate_classes_accuracy,
    calculate_teachers_performance,
    calculate_student_weekly_accuracy,
    calculate_student_accuracy_by_lesson,
)

# Chart generation
from app.utils.analytics.GUI.analytics_GUI import (
    show_students_accuracy,
    show_classes_accuracy,
    show_teachers_performance,
    show_student_weekly_accuracy,
    show_student_accuracy_by_lesson,
)

# Models and utilities
from app.models.models import School, Student, Class
from app.server_side.Website.send_email import send_styled_email

# Initialize the Blueprint for analytics-related routes
bp = Blueprint('analytics_routes', __name__)


def get_school_email() -> str:
    """
    Get the current school's email address from the database.

    Returns:
        str: Email address of the logged-in user's school.
    """
    return School.query.filter(School.id == current_user.id).first().email


@bp.route('/panel/analytics')
@login_required
def analytics_menu():
    """
    Display the main analytics dashboard with available report options.
    """
    return render_template("analytics/analytics_menu.html")


@bp.route('/panel/analytics/compare_students', methods=['GET', 'POST'])
@login_required
def compare_students():
    """
    Compare students' performance within a class.

    GET:
        - Render a form to select a class.

    POST:
        - Calculate student accuracies.
        - Generate a PDF bar chart report.
        - Send the report via email.
    """
    if request.method == "POST":
        # Extract class ID from form
        class_id = request.form['selected_class']

        # Generate accuracy data and save the chart
        data = calculate_students_accuracy(str(class_id))
        show_students_accuracy(data)

        # Send the report via email in background
        Thread(target=send_styled_email,
               args=(get_school_email(), 'Compare Students',
                     r"c:\sap-project\server\compare_students.pdf")
               ).start()

        return redirect(url_for("analytics_routes.analytics_menu"))

    # Render the class selection page
    classes = Class.query.filter(Class.school_id == current_user.id).all()
    return render_template('analytics/class_name_for_compare_students.html', classes=classes)


@bp.route('/panel/analytics/compare_classes')
@login_required
def compare_classes():
    """
    Compare overall performance between all classes in the school.

    - Generates a bar chart report and emails it to the school.
    """
    data = calculate_classes_accuracy()
    show_classes_accuracy(data)

    Thread(target=send_styled_email,
           args=(get_school_email(), 'Compare Classes',
                 r"c:\sap-project\server\compare_classes.pdf")
           ).start()

    return redirect(url_for("analytics_routes.analytics_menu"))


@bp.route('/panel/analytics/compare_teachers')
@login_required
def compare_teachers():
    """
    Compare performance metrics between all teachers in the school.

    - Generates a bar chart report and emails it to the school.
    """
    data = calculate_teachers_performance()
    show_teachers_performance(data)

    Thread(target=send_styled_email,
           args=(get_school_email(), 'Compare Teachers',
                 r"c:\sap-project\server\compare_teachers.pdf")
           ).start()

    return redirect(url_for("analytics_routes.analytics_menu"))


@bp.route('/panel/analytics/student_accuracy_week', methods=['GET', 'POST'])
@login_required
def student_accuracy_week():
    """
    Show a student's daily accuracy trend over the past 7 days.

    GET:
        - Render a form to input the student's national code.

    POST:
        - Generate a line chart showing daily accuracy.
        - Save as PDF and send to school email.
    """
    if request.method == "POST":
        # Retrieve student from national code
        student = Student.query.filter(
            Student.student_national_code == request.form['student_national_code']
        ).first()

        if student:
            # Calculate accuracy and generate report
            data = calculate_student_weekly_accuracy(
                str(student.class_id), str(student.id)
            )
            show_student_weekly_accuracy(
                f"{student.student_name} {student.student_family}", data)

            Thread(target=send_styled_email,
                   args=(get_school_email(), 'Weekly Accuracy',
                         r"c:\sap-project\server\student_accuracy_week.pdf")
                   ).start()

        return redirect(url_for("analytics_routes.analytics_menu"))

    return render_template("analytics/student_nc_for_accuracy_week.html")


@bp.route('/panel/analytics/student_accuracy_by_lesson', methods=['GET', 'POST'])
@login_required
def student_accuracy_by_lesson():
    """
    Show a student's accuracy performance per lesson.

    GET:
        - Render a form to input the student's national code.

    POST:
        - Generate a bar chart comparing accuracy across lessons.
        - Save as PDF and send to school email.
    """
    if request.method == "POST":
        student = Student.query.filter(
            Student.student_national_code == request.form['student_national_code']
        ).first()

        if student:
            # Calculate per-lesson accuracy and generate chart
            data = calculate_student_accuracy_by_lesson(
                str(student.class_id), str(student.id)
            )
            show_student_accuracy_by_lesson(
                f"{student.student_name} {student.student_family}", data)

            Thread(target=send_styled_email,
                   args=(get_school_email(), 'Accuracy By Lesson',
                         r"c:\sap-project\server\student_accuracy_by_lesson.pdf")
                   ).start()

        return redirect(url_for("analytics_routes.analytics_menu"))

    return render_template("analytics/student_nc_for_accuracy_lesson.html")
