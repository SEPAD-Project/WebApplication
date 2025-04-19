from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import login_required, current_user
from threading import Thread

# Import analytics calculation and visualization functions
from app.utils.analytics.Generator.analytics_Generator import *
from app.utils.analytics.GUI.analytics_GUI import *

# Import models and utilities
from app.utils.generate_class_code import reverse_class_code
from app.models.models import School, Student
from app.server_side.Website.send_email import send_styled_email


bp = Blueprint('analytics_routes', __name__)  # Create Flask Blueprint


def get_school_email() -> str:
    """Returns the email of the current user's school (cached query)"""
    return School.query.filter(School.id == current_user.id).first().email


@bp.route('/panel/analytics')
@login_required
def analytics_menu():
    """Main analytics dashboard - shows available report options"""
    return render_template("analytics/analytics_menu.html")


@bp.route('/panel/analytics/compare_students', methods=['GET', 'POST'])
@login_required
def compare_students():
    """Compare students within a class"""
    if request.method == "POST":
        # Process form submission
        class_id = request.form['selected_class']
        data = calculate_students_accuracy(str(class_id))

        # Generate PDF and email it
        show_students_accuracy(data)
        Thread(target=send_styled_email,
               args=(get_school_email(), 'Compare Students',
                     r"c:\sap-project\server\compare_students.pdf")
               ).start()

        return redirect(url_for("analytics_routes.analytics_menu"))

    # Show class selection form
    classes = Class.query.filter(
        Class.school_id == current_user.id).all()
    return render_template('analytics/class_name_for_compare_students.html', classes=classes)


@bp.route('/panel/analytics/compare_classes')
@login_required
def compare_classes():
    """School-wide class performance comparison"""
    data = calculate_classes_accuracy()
    show_classes_accuracy(data)

    # Async email with report
    Thread(target=send_styled_email,
           args=(get_school_email(), 'Compare Classes',
                 r"c:\sap-project\server\compare_classes.pdf")
           ).start()

    return redirect(url_for("analytics_routes.analytics_menu"))


@bp.route('/panel/analytics/compare_teachers')
@login_required
def compare_teachers():
    """Teacher performance comparison"""
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
    """Weekly accuracy trend for individual student"""
    if request.method == "POST":
        student = Student.query.filter(
            Student.student_national_code == request.form['student_national_code']
        ).first()

        if student:
            # Generate and send report
            data = calculate_student_weekly_accuracy(
                str(student.class_id),
                str(student.id)
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
    """Lesson-based accuracy for individual student"""
    if request.method == "POST":
        student = Student.query.filter(
            Student.student_national_code == request.form['student_national_code']
        ).first()

        if student:
            # Generate and send report
            data = calculate_student_accuracy_by_lesson(
                str(student.class_id),
                str(student.id)
            )
            show_student_accuracy_by_lesson(
                f"{student.student_name} {student.student_family}", data)

            Thread(target=send_styled_email,
                   args=(get_school_email(), 'Accuracy By Lesson',
                         r"c:\sap-project\server\student_accuracy_by_lesson.pdf")
                   ).start()

        return redirect(url_for("analytics_routes.analytics_menu"))

    return render_template("analytics/student_nc_for_accuracy_lesson.html")
