# Standard library imports
import os
import shutil
import zipfile

# Third-party library imports
from flask import Blueprint, redirect, render_template, request, url_for, session
from flask_login import current_user, login_required

# Internal module imports
from app import db  # SQLAlchemy instance for database operations
from app.models.models import Student, Class, School
from app.server_side.Website.directory_manager import (
    dm_create_student,
    dm_delete_student
)
from app.utils.excel_reading import add_students
# Utility to reverse-engineer class code
from app.utils.generate_class_code import reverse_class_code


# Create a new Blueprint for all student-related routes
bp = Blueprint('student_routes', __name__)


@bp.route('/panel/students')
@login_required
def panel_students():
    """
    Displays all students of the logged-in user's school.
    - If a search query (q) is provided, filters students by name, family name, or national code.
    - Otherwise, displays all students from the school.
    """
    school = School.query.filter(School.id==current_user.id).first()
    query = request.args.get('q')
    if query:
        students = Student.query.filter(
            ((Student.student_name.ilike(f"%{query}%")) |
             (Student.student_family.ilike(f"%{query}%")) |
             (Student.student_national_code.ilike(f"%{query}%"))) &
            (Student.school_id == current_user.id)
        ).all()
    else:
        students = school.students

    return render_template('student/students.html', students=students)


@bp.route('/panel/students/add_student', methods=['GET', 'POST'])
@login_required
def add_student():
    """
    Handles the creation of a new student via form submission.
    - GET: Renders the form.
    - POST: Saves new student data in the database and file system.
    """
    if request.method == 'POST':
        # Extract form data
        student_name = request.form['student_name']
        student_family = request.form['student_family']
        student_national_code = request.form['student_national_code']
        student_password = request.form['student_password']
        class_id = request.form['selected_class']
        student_image = request.files['file_input']

        # Create and save the new student
        new_student = Student(
            student_name=student_name,
            student_family=student_family,
            student_national_code=student_national_code,
            student_password=student_password,
            class_id=class_id,
            school_id=current_user.id
        )
        try:
            db.session.add(new_student)
            db.session.commit()

            # Save the student image
            image_path = f"c:/sap-project/server/schools/{str(current_user.id)}/{str(class_id)}/{str(new_student.id)}.jpg"
            student_image.save(image_path)

            dm_create_student(
                school_id=str(current_user.id),
                class_id=str(class_id),
                student_id=str(new_student.id)
            )

            return redirect(url_for('student_routes.panel_students'))
        except Exception:
            db.session.rollback()
            session["show_error_notif"] = True
            return redirect(url_for('student_routes.duplicated_student_info'))

    # Render the form with available classes
    school = School.query.filter(School.id==current_user.id).first()
    return render_template('student/add_student.html', classes=school.classes)


@bp.route('/panel/students/add_from_excel', methods=['GET', 'POST'])
@login_required
def add_from_excel():
    """
    Reads student data from an Excel file and adds them in bulk.
    - Handles file saving, data extraction, validation, and database commit.
    - Redirects to error pages if issues occur.
    """
    if request.method == 'POST':
        global texts

        school = School.query.filter(School.id==current_user.id).first()

        # Prepare references for validation
        classes = school.classes
        class_names = [c.class_name for c in classes]
        students = school.students
        existing_ncs = [s.student_national_code for s in students]

        # Read file and mapping from user input
        excel_file = request.files["file_input"]
        zip_file = request.files["zip_input"]
        sheet_name = request.form["sheet"]
        name_letter = request.form["name"]
        family_letter = request.form["family"]
        nc_letter = request.form["national_code"]
        class_letter = request.form["class"]
        pass_letter = request.form["password"]

        excel_path = f"c:/sap-project/server/schools/{str(current_user.id)}/students.xlsx"
        try:
            excel_file.save(excel_path)
        except PermissionError:
            session["show_error_notif"] = True
            return redirect(url_for("student_routes.file_permission_error"))

        result = add_students(
            excel_path, sheet_name,
            name_letter, family_letter, nc_letter,
            class_letter, pass_letter,
            class_names, existing_ncs
        )
        os.remove(excel_path)

        # Handle different result outcomes
        if result == 'sheet_not_found':
            session["show_error_notif"] = True
            texts = ["Please review your input for sheet name."]
            return redirect(url_for("student_routes.error_in_excel"))
        
        if result == 'bad_column_letter':
            session["show_error_notif"] = True
            texts = ["Please review your input for column letters."]
            return redirect(url_for("student_routes.error_in_excel"))

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

        # Process the ZIP file containing student images
        zip_path = f"c:/sap-project/server/schools/{str(current_user.ip)}/student_ref_images.zip"
        extracted_files_path = zip_path[:-4]
        zip_file.save(zip_path)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extracted_files_path)

        # Add validated students to the database
        for student in result:
            class_id = Class.query.filter(Class.class_code==student['class']).first().id
            new_student = Student(
                student_name=student['name'],
                student_family=student['family'],
                student_national_code=student['national_code'],
                class_id=class_id,
                student_password=student['password'],
                school_code=current_user.id
            )
            db.session.add(new_student)

            try:
                shutil.move(
                    f"{extracted_files_path}/{reverse_class_code(student['class'])[1]}/{student['national_code']}.jpg",
                    f"c:/sap-project/server/schools/{str(current_user.id)}/{str(class_id)}"
                )
            except FileNotFoundError:
                texts = [
                    f"Cannot find image for student with national code '{student['national_code']}' in your ZIP file."]
                session["show_error_notif"] = True
                return redirect(url_for("student_routes.error_in_excel"))

            dm_create_student(
                school_id=(current_user.id),
                class_id=str(class_id),
                student_id=new_student.id
            )

        db.session.commit()
        shutil.rmtree(extracted_files_path)
        os.remove(zip_path)
        return redirect(url_for("student_routes.panel_students"))

    return render_template("student/add_from_excel.html")


@bp.route('/panel/students/edit_student/<student_national_code>', methods=['GET', 'POST'])
@login_required
def edit_student(student_national_code):
    """
    Edits a specific student's information.
    - GET: Displays the form with current student data.
    - POST: Applies updates to the database and directory.
    """
    school = School.query.filter(School.id==current_user.id).first()
    student = Student.query.filter(Student.school_id==school.id & Student.student_national_code==student_national_code).first()
    if not student in school.students:
        session["show_error_notif"] = True
        return redirect(url_for("student_routes.unknown_student_info"))

    if request.method == "POST":
        student.student_name = request.form['student_name']
        student.student_family = request.form['student_family']
        student.student_national_code = request.form['student_national_code']
        student.student_password = request.form['student_password']

        try:
            db.session.commit()
            return redirect(url_for('student_routes.panel_students'))
        except Exception:
            db.session.rollback()
            session["show_error_notif"] = True
            return redirect(url_for('student_routes.duplicated_student_info'))

    return render_template('student/edit_student.html', student=student, classes=school.classes)


@bp.route('/panel/students/remove_student/<student_national_code>', methods=['POST', 'GET'])
@login_required
def remove_student(student_national_code):
    """
    Deletes a student from the database and filesystem.
    """
    school = School.query.filter(School.id==current_user.id).first()
    student = Student.query.filter(
        Student.student_national_code==student_national_code & Student.school_id==school.id
    ).first()

    if not student in school.classes:
        session["show_error_notif"] = True
        return redirect(url_for("student_routes.unknown_student_info"))

    dm_delete_student(
        school_id=str(current_user.id),
        class_id=str(student.class_id),
        student_id=str(student.id)
    )
    db.session.delete(student)
    db.session.commit()

    return redirect(url_for('student_routes.panel_students'))


@bp.route('/panel/students/student_info/<student_national_code>')
@login_required
def student_info(student_national_code):
    """
    Displays detailed information about a student.
    """
    school = School.query.filter(School.id==current_user.id).first()
    student = Student.query.filter(
        Student.student_national_code==student_national_code & Student.school_id==school.id
    ).first()

    if not student in school.students:
        session["show_error_notif"] = True
        return redirect(url_for("student_routes.unknown_student_info"))

    return render_template('student/student_info.html', data=student)


# Error Handling Routes
@bp.route("/panel/students/unknown_student_info", methods=['GET', 'POST'])
@login_required
def unknown_student_info():
    """
    Renders an error page when a student is not found.
    """
    if not session.pop('show_error_notif', False):
        return redirect(url_for('student_routes.panel_students'))
    return render_template('student/unknown_student_info.html')


@bp.route("/panel/students/duplicated_student_info", methods=['GET', 'POST'])
@login_required
def duplicated_student_info():
    """
    Renders an error page when duplicate student data is detected.
    """
    if not session.pop('show_error_notif', False):
        return redirect(url_for('student_routes.add_student'))
    return render_template('student/duplicated_student_info.html')


@bp.route("/panel/students/error_in_excel", methods=['GET', 'POST'])
@login_required
def error_in_excel():
    """
    Renders an error page when issues are found in the Excel file.
    """
    if not session.pop('show_error_notif', False):
        return redirect(url_for('student_routes.add_from_excel'))
    return render_template('student/error_in_excel.html', texts=texts)


@bp.route('/panel/students/file_permission_error')
@login_required
def file_permission_error():
    """
    Renders an error page when the Excel file cannot be saved due to permissions.
    """
    if not session.pop('show_error_notif', False):
        return redirect(url_for('student_routes.add_from_excel'))
    return render_template('student/file_permission_error.html')
