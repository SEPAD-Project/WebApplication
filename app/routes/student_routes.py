# Import necessary internal modules and utilities
from app import db  # SQLAlchemy instance for database operations

from app.models._class import Class  # Importing the Class model
from app.models.student import Student  # Importing the Student model

from app.utils.generate_class_code import reverse_class_code  # Utility to reverse-engineer class code (get class name from code)

# Student directory management utilities for file system operations
from app.server_side.Website.directory_manager import (
    dm_create_student,
    dm_edit_student,
    dm_delete_student
)

# Utility to bulk add students by reading Excel files
from app.utils.excel_reading import add_students

# Flask-related imports
from flask import Blueprint, g, redirect, render_template, request, url_for, session
from flask_login import current_user, login_required  # For session-based login checking

import zipfile
import shutil

# Create a new Blueprint for all student-related routes
bp = Blueprint('student_routes', __name__)


@bp.route('/panel/students')
@login_required
def panel_students():
    """
    Route: /panel/students
    Description:
        Displays all students of the logged-in user's school.
        - If a search query (q) is given, filters students by name, family name, or national code.
        - Otherwise, displays all students from the database.
    """
    query = request.args.get('q')

    if query:
        # Perform a filtered search across student name, family, and national code
        students = Student.query.filter(
            ((Student.student_name.ilike(f"%{query}%")) |
             (Student.student_family.ilike(f"%{query}%")) |
             (Student.student_national_code.ilike(f"%{query}%"))) &
            (Student.school_code == current_user.school_code)
        ).all()
    else:
        # No query → fetch all students from current user's school
        students = Student.query.filter(Student.school_code == current_user.school_code).all()

    return render_template('student/students.html', students=students)


@bp.route("/panel/students/add_student", methods=['GET', 'POST'])
@login_required
def add_student():
    """
    Route: /panel/students/add_student
    Description:
        Handles the creation of a new student via form submission.
        - GET: Show the form.
        - POST: Save new student data in the database and file system.
    """
    if request.method == 'POST':
        # Extract student data from the form
        student_name = request.form['student_name']
        student_family = request.form['student_family']
        student_national_code = request.form['student_national_code']
        student_password = request.form['student_password']
        class_code = request.form['selected_class']
        school_code = current_user.school_code
        student_image = request.files['file_input']
        student_image.save(f"c:\sap-project\server\schools\{school_code}\{reverse_class_code(class_code)[1]}\{student_national_code}.jpg")

        # Construct new Student object
        new_student = Student(student_name, student_family,
                              student_national_code, student_password,
                              class_code, school_code)

        try:
            # Try to save the new student to the database
            db.session.add(new_student)
            db.session.commit()

            # Also create the student's folder in the file system
            dm_create_student(
                school_code=school_code,
                class_name=reverse_class_code(class_code)[1],
                student_code=student_national_code
            )
        except:
            # Handle case where student info (e.g., national code) already exists
            db.session.rollback()
            session["show_error_notif"] = True
            return redirect(url_for('student_routes.duplicated_student_info'))

        return redirect(url_for('student_routes.panel_students'))

    # If GET request → render the form
    classes = Class.query.filter(Class.school_code == current_user.school_code).all()
    return render_template('student/add_student.html', classes=classes)


@bp.route("/panel/students/add_from_excel", methods=['GET', 'POST'])
@login_required
def add_from_excel():
    """
    Route: /panel/students/add_from_excel
    Description:
        Reads student data from an Excel file and adds them in bulk.
        - Handles file saving, data extraction, validation, and database commit.
        - Redirects to error pages if problems occur (e.g., invalid format, duplicates).
    """
    if request.method == 'POST':
        global texts

        # Prepare references for validation
        classes = Class.query.filter(Class.school_code == current_user.school_code).all()
        class_names = [c.class_name for c in classes]

        students = Student.query.filter(Student.school_code == current_user.school_code).all()
        existing_ncs = [s.student_national_code for s in students]

        # Read file and mapping from user input
        file = request.files["file_input"]
        zip_file = request.files["zip_input"]
        sheet_name = request.form["sheet"]
        name_letter = request.form["name"]
        family_letter = request.form["family"]
        nc_letter = request.form["national_code"]
        class_letter = request.form["class"]
        pass_letter = request.form["password"]

        try:
            file.save("students.xlsx")
        except PermissionError:
            session["show_error_notif"] = True
            return redirect(url_for("student_routes.file_permission_error"))

        result = add_students(
            'students.xlsx', sheet_name,
            name_letter, family_letter, nc_letter,
            class_letter, pass_letter,
            class_names, existing_ncs
        )

        # Handle different result outcomes
        if result == 'sheet_not_found':
            session["show_error_notif"] = True
            return redirect(url_for("student_routes.error_in_excel", text="Please review your input for sheet name."))
        
        if result == 'bad_column_letter':
            session["show_error_notif"] = True
            return redirect(url_for("student_routes.error_in_excel", text="Please review your input for column letters."))

        if isinstance(result[0], list):
            texts = []
            for problem in result:
                col_msg = f"Please review the cell {problem[2]}{problem[1]}"
                if problem[0] == "bad_format":
                    texts.append(f"{col_msg} because of bad data format.")
                elif problem[0] == "duplicated_nc":
                    texts.append(f"{col_msg} due to duplicated national code.")
                elif problem[0] == 'unknown_class':
                    texts.append(f"{col_msg} due to unknown class name.")
                else:
                    texts.append(f"{col_msg} due to an unknown issue.")
            session["show_error_notif"] = True
            return redirect(url_for("student_routes.error_in_excel"))
        

        zip_path = f'c:\sap-project\server\schools\{current_user.school_code}\student_ref_images.zip'
        zip_file.save(zip_path)

        extracted_files_path = zip_path[:-4]

        with zipfile.ZipFile(zip_path, 'r') as zip:  
            zip.extractall(extracted_files_path)


        # Add validated students to the database
        for student in result:
            new_student = Student(
                student_name=student['name'],
                student_family=student['family'],
                student_national_code=student['national_code'],
                class_code=student['class'],
                student_password=student['password'],
                school_code=current_user.school_code
            )
            db.session.add(new_student)

            try:
                shutil.move(f"{extracted_files_path}\{reverse_class_code(student['class'])[1]}\{student['national_code']}.jpg", f"c:\sap-project\server\schools\{current_user.school_code}\{reverse_class_code(student['class'])[1]}")
            except:
                texts = [f"can't find image for student with national code '{student['national_code']}' in your zip file."]
                session["show_error_notif"] = True
                return redirect(url_for("student_routes.error_in_excel"))

            dm_create_student(current_user.school_code, reverse_class_code(student['class'])[1], student['national_code'])

        db.session.commit()
        shutil.rmtree(extracted_files_path)
        return redirect(url_for("student_routes.panel_students"))

    return render_template("student/add_from_excel.html")


@bp.route("/panel/students/edit_student/<student_national_code>", methods=['GET', 'POST'])
@login_required
def edit_student(student_national_code):
    """
    Route: /panel/students/edit_student/<student_national_code>
    Description:
        Edits a specific student's information.
        - GET: Displays the form with current student data.
        - POST: Applies updates to the database and directory.
    """
    if request.method == "POST":
        new_name = request.form['student_name']
        new_family = request.form['student_family']
        new_national_code = request.form['student_national_code']
        new_password = request.form['student_password']

        student = Student.query.filter(
            (Student.student_national_code == student_national_code) &
            (Student.school_code == current_user.school_code)
        ).first()

        if student is None:
            session["show_error_notif"] = True
            return redirect(url_for("student_routes.unknown_student_info"))

        student.student_name = new_name
        student.student_family = new_family
        student.student_national_code = new_national_code
        student.student_password = new_password

        try:
            db.session.commit()
            dm_edit_student(
                school_code=current_user.school_code,
                class_name=reverse_class_code(student.class_code)[1],
                old_student_code=student_national_code,
                new_student_code=new_national_code
            )
        except:
            db.session.rollback()
            session["show_error_notif"] = True
            return redirect(url_for('student_routes.duplicated_student_info'))

        return redirect(url_for('student_routes.panel_students'))

    classes = Class.query.filter(Class.school_code == current_user.school_code).all()
    student = Student.query.filter(
        (Student.student_national_code == student_national_code) &
        (Student.school_code == current_user.school_code)
    ).first()

    if student is None:
        session["show_error_notif"] = True
        return redirect(url_for("student_routes.unknown_student_info"))

    return render_template('student/edit_student.html', student=student, classes=classes)


@bp.route("/panel/students/remove_student/<student_national_code>", methods=['POST', 'GET'])
@login_required
def remove_student(student_national_code):
    """
    Route: /panel/students/remove_student/<student_national_code>
    Description:
        Deletes a student from the database and filesystem.
    """
    student = Student.query.filter(
        (Student.student_national_code == student_national_code) &
        (Student.school_code == current_user.school_code)
    ).first()

    if student is None:
        session["show_error_notif"] = True
        return redirect(url_for("student_routes.unknown_student_info"))

    db.session.delete(student)
    db.session.commit()

    dm_delete_student(
        school_code=current_user.school_code,
        class_name=reverse_class_code(student.class_code)[1],
        student_code=student_national_code
    )

    return redirect(url_for('student_routes.panel_students'))


@bp.route("/panel/students/student_info/<student_national_code>")
@login_required
def student_info(student_national_code):
    """
    Route: /panel/students/student_info/<student_national_code>
    Description:
        Displays detailed information about a student.
    """
    student = Student.query.filter(
        (Student.student_national_code == student_national_code) &
        (Student.school_code == current_user.school_code)
    ).first()

    if student is None:
        session["show_error_notif"] = True
        return redirect(url_for("student_routes.unknown_student_info"))

    return render_template('student/student_info.html', data=student)


# Error Handling Routes


@bp.route("/panel/students/unknown_student_info", methods=['GET', 'POST'])
@login_required
def unknown_student_info():
    """
    Renders an error page when student is not found.
    """
    if not session.get('show_error_notif', False):
        return redirect(url_for('student_routes.panel_students'))
    session.pop('show_error_notif', None)
    return render_template('student/unknown_student_info.html')


@bp.route("/panel/students/duplicated_student_info", methods=['GET', 'POST'])
@login_required
def duplicated_student_info():
    """
    Renders an error page when duplicate student data is detected.
    """
    if not session.get('show_error_notif', False):
        return redirect(url_for('student_routes.add_student'))
    session.pop('show_error_notif', None)
    return render_template('student/duplicated_student_info.html')


@bp.route("/panel/students/error_in_excel/", methods=['GET', 'POST'])
@login_required
def error_in_excel():
    """
    Renders an error page when issues are found in the Excel file.
    """
    if not session.get('show_error_notif', False):
        return redirect(url_for('student_routes.add_from_excel'))
    session.pop('show_error_notif', None)
    return render_template('student/error_in_excel.html', texts=texts)


@bp.route('/panel/students/file_permission_error')
@login_required
def file_permission_error():
    """
    Renders an error page when the Excel file cannot be saved due to permissions.
    """
    if not session.get('show_error_notif', False):
        return redirect(url_for('student_routes.add_from_excel'))
    session.pop('show_error_notif', None)
    return render_template('student/file_permission_error.html')
