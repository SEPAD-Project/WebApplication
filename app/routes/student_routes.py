# Import necessary modules
from app import db
from app.models._class import Class
from app.models.student import Student

from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required

# Initialize the Blueprint for student-related routes
bp = Blueprint('student_routes', __name__)


@bp.route('/panel/students')
@login_required
def go_to_panel_students():
    """
    Displays the list of students in the panel.
    - Filters students by name, family, or national code if a query is provided.
    - Shows all students if no query is provided.
    """
    # Retrieve the search query from the request arguments
    query = request.args.get('q')

    if query:
        # Filter students by name, family, or national code based on the query
        students = Student.query.filter(
            ((Student.student_name.ilike(f"%{query}%")) |
             (Student.student_family.ilike(f"%{query}%")) |
             (Student.student_national_code.ilike(f"%{query}%"))) &
            (Student.school_code == current_user.school_code)
        ).all()
    else:
        # Retrieve all students for the current school if no query is provided
        students = Student.query.filter(Student.school_code == current_user.school_code).all()

    # Render the HTML page displaying the list of students
    return render_template('student/students.html', students=students)


@bp.route("/panel/students/add_student", methods=['GET', 'POST'])
@login_required
def go_to_add_student():
    """
    Handles adding a new student in the panel.
    - For POST requests, processes form data and adds the new student to the database.
    - For GET requests, renders the form for adding a new student.
    """
    if request.method == 'POST':
        # Retrieve form data
        student_name = request.form['student_name']
        student_family = request.form['student_family']
        student_national_code = request.form['student_national_code']
        student_password = request.form['student_password']
        class_code = request.form['selected_class']
        school_code = current_user.school_code

        # Create a new Student object with the provided data
        new_student = Student(student_name, student_family,
                              student_national_code, student_password, class_code, school_code)

        try:
            # Add the new student to the database
            db.session.add(new_student)
            db.session.commit()
        except:
            # Rollback changes and redirect to an error page if unique constraints are violated
            db.session.rollback()
            return redirect(url_for('student_routes.go_to_duplicated_student_info'))

        # Redirect to the student list page after successful registration
        return redirect(url_for('student_routes.go_to_panel_students'))

    # Render the form for adding a new student
    classes = Class.query.filter(Class.school_code == current_user.school_code).all()
    return render_template('student/add_student.html', classes=classes)


@bp.route("/panel/students/edit_student/<student_national_code>", methods=['GET', 'POST'])
@login_required
def go_to_edit_student(student_national_code):
    """
    Handles editing an existing student in the panel.
    - For POST requests, updates the student details in the database.
    - For GET requests, renders the form for editing the student.
    """
    if request.method == "POST":
        # Retrieve updated data from the form
        new_name = request.form['student_name']
        new_family = request.form['student_family']
        new_national_code = request.form['student_national_code']
        new_password = request.form['student_password']
        new_class = request.form['selected_class']

        # Find the student in the database
        student = Student.query.filter(Student.student_national_code == student_national_code).first()

        # Update the student's information
        student.student_name = new_name
        student.student_family = new_family
        student.student_national_code = new_national_code
        student.student_password = new_password
        student.class_code = new_class

        try:
            # Commit the changes to the database
            db.session.commit()
        except:
            # Rollback changes and redirect to an error page if unique constraints are violated
            db.session.rollback()
            return redirect(url_for('student_routes.go_to_duplicated_student_info'))

        # Redirect to the student list page after successful update
        return redirect(url_for('student_routes.go_to_panel_students'))

    # Render the form for editing the student
    classes = Class.query.filter(Class.school_code == current_user.school_code).all()
    student = Student.query.filter((Student.student_national_code == student_national_code) &
                                   (Student.school_code == current_user.school_code)).first()
    return render_template('student/edit_student.html', student=student, classes=classes)


@bp.route("/panel/students/remove_student/<student_national_code>", methods=['POST', 'GET'])
@login_required
def go_to_remove_student(student_national_code):
    """
    Handles removing a student from the panel.
    - Deletes the student record from the database.
    """
    # Find the student in the database
    student = Student.query.filter((Student.student_national_code == student_national_code) &
                                   (Student.school_code == current_user.school_code)).first()

    # Delete the student record and commit changes
    db.session.delete(student)
    db.session.commit()

    # Redirect to the student list page after successful deletion
    return redirect(url_for('student_routes.go_to_panel_students'))


@bp.route("/panel/students/student_info/<student_national_code>")
@login_required
def go_to_student_info(student_national_code):
    """
    Displays detailed information about a specific student.
    """
    # Find the student in the database
    student = Student.query.filter((Student.student_national_code == student_national_code) &
                                   (Student.school_code == current_user.school_code)).first()

    # Render the student info page with the retrieved data
    return render_template('student/student_info.html', data=student)


@bp.route("/panel/students/duplicated_student_info", methods=['GET', 'POST'])
@login_required
def go_to_duplicated_student_info():
    """
    Displays an error page for duplicated student information.
    """
    return render_template('student/duplicated_student_info.html')