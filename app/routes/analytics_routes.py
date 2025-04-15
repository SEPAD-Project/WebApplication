from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import login_required, current_user
from threading import Thread

# Import analytics calculation and visualization functions
from app.utils.analytics.Generator.analytics_Generator import *
from app.utils.analytics.GUI.analytics_GUI import *

# Import models and utilities
from app.utils.generate_class_code import reverse_class_code
from app.models.school import School
from app.models.student import Student
from app.server_side.Website.send_email import send_styled_email


bp = Blueprint('analytics_routes', __name__)  # Create Flask Blueprint


def get_school_email() -> str:
    """Returns the email of the current user's school (cached query)"""
    return School.query.filter(School.school_code == current_user.school_code).first().email


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
        class_name = reverse_class_code(request.form['selected_class'])[1]
        data = calculate_students_accuracy(class_name)

        # Generate PDF and email it
        show_students_accuracy(data)
        Thread(target=send_styled_email,
               args=(get_school_email(), 'Compare Students',
                     r"c:\sap-project\server\compare_students.pdf")
               ).start()

        return redirect(url_for("analytics_routes.analytics_menu"))

    # Show class selection form
    classes = Class.query.filter(
        Class.school_code == current_user.school_code).all()
    return render_template('analytics/compare_students_form.html', classes=classes)


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
                reverse_class_code(student.class_code)[1],
                student.student_national_code
            )
            show_student_weekly_accuracy(
                f"{student.student_name} {student.student_family}", data)

            Thread(target=send_styled_email,
                   args=(get_school_email(), 'Weekly Accuracy',
                         r"c:\sap-project\server\student_accuracy_week.pdf")
                   ).start()

        return redirect(url_for("analytics_routes.analytics_menu"))

    return render_template("analytics/student_weekly_form.html")


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
                reverse_class_code(student.class_code)[1],
                student.student_national_code
            )
            show_student_accuracy_by_lesson(
                f"{student.student_name} {student.student_family}", data)

            Thread(target=send_styled_email,
                   args=(get_school_email(), 'Accuracy By Lesson',
                         r"c:\sap-project\server\student_accuracy_by_lesson.pdf")
                   ).start()

        return redirect(url_for("analytics_routes.analytics_menu"))

    return render_template("analytics/student_lessons_form.html")
