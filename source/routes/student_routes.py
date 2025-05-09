# Standard Library Imports
import os
import shutil
import zipfile

# Third-party Imports
from flask import Blueprint, redirect, render_template, request, url_for, session
from flask_login import current_user, login_required

# Internal Application Imports
from source import db
from source.models.models import Student, Class, School
from source.server_side.Website.directory_manager import dm_create_student, dm_delete_student, dm_edit_student
from source.utils.excel_reading import add_students
from source.utils.generate_class_code import reverse_class_code

# Create a new Blueprint for all student-related routes
bp = Blueprint('student_routes', __name__)


@bp.route('/panel/students')
@login_required
def panel_students():
    """
    Display all students belonging to the logged-in user's school.

    If a search query is provided (via ?q=...), filter students by:
    - First name
    - Last name
    - National code

    Returns:
        Rendered HTML page with a list of students.
    """
    school = School.query.filter(School.id == current_user.id).first()
    query = request.args.get('q')

    if query:
        # Filter students based on search query
        students = Student.query.filter(
            ((Student.student_name.ilike(f"%{query}%")) |
             (Student.student_family.ilike(f"%{query}%")) |
             (Student.student_national_code.ilike(f"%{query}%"))) &
            (Student.school_id == current_user.id)
        ).all()
    else:
        # Return all students in the school
        students = school.students

    return render_template('student/students.html', students=students)


@bp.route('/panel/students/add_student', methods=['GET', 'POST'])
@login_required
def add_student():
    """
    Handle creation of a new student via form submission.

    GET:
        - Render the student creation form.

    POST:
        - Receive form data and create a new student in the database.
        - Save the student image file.
        - Create necessary directory structure.

    Returns:
        Redirect to the student list or show error on failure.
    """
    if request.method == 'POST':
        # Extract form inputs
        student_name = request.form['student_name']
        student_family = request.form['student_family']
        student_national_code = request.form['student_national_code']
        student_password = request.form['student_password']
        class_id = request.form['selected_class']
        student_image = request.files['file_input']

        # Create Student instance
        new_student = Student(
            student_name=student_name,
            student_family=student_family,
            student_national_code=student_national_code,
            student_password=student_password,
            class_id=class_id,
            school_id=current_user.id
        )

        # Save student to database
        db.session.add(new_student)
        db.session.commit()

        # Save student image file
        image_path = f"c:/sap-project/server/schools/{str(current_user.id)}/{str(class_id)}/{str(new_student.student_national_code)}.jpg"
        student_image.save(image_path)

        # Create directory for the student
        dm_create_student(
            school_id=str(current_user.id),
            class_id=str(class_id),
            student_code=str(new_student.student_national_code)
        )

        return redirect(url_for('student_routes.panel_students'))


    # GET: Render form with available classes
    school = School.query.filter(School.id == current_user.id).first()
    return render_template('student/add_student.html', classes=school.classes)


@bp.route('/panel/students/add_from_excel', methods=['GET', 'POST'])
@login_required
def add_from_excel():
    """
    Handle bulk student import from an Excel file.

    GET:
        - Render the upload form.

    POST:
        - Save uploaded Excel and ZIP files.
        - Validate and parse Excel data.
        - Handle known Excel-related errors.
        - Extract student images from ZIP.
        - Add validated students and associate their image files.

    Returns:
        Redirect to student list or an error page.
    """
    if request.method == 'POST':
        school = School.query.filter(School.id == current_user.id).first()

        # Gather existing data for validation
        classes = school.classes
        class_names = [c.class_name for c in classes]
        students = school.students
        existing_ncs = [s.student_national_code for s in students]

        # Get form inputs and files
        excel_file = request.files["file_input"]
        zip_file = request.files["zip_input"]
        sheet_name = request.form["sheet"]
        name_letter = request.form["name"]
        family_letter = request.form["family"]
        nc_letter = request.form["national_code"]
        class_letter = request.form["class"]
        pass_letter = request.form["password"]

        # Save Excel file to disk
        excel_path = f"c:/sap-project/server/schools/{str(current_user.id)}/students.xlsx"
        try:
            excel_file.save(excel_path)
        except PermissionError:
            session["show_error_notif"] = True
            return redirect(url_for("student_routes.file_permission_error"))

        # Parse and validate Excel file
        result = add_students(
            excel_path, sheet_name,
            name_letter, family_letter, nc_letter,
            class_letter, pass_letter,
            class_names, existing_ncs
        )
        os.remove(excel_path)

        # Handle known Excel validation errors
        if result == 'sheet_not_found':
            session["show_error_notif"] = True
            session["excel_errors"] = [
                "Please review your input for sheet name."]
            return redirect(url_for("student_routes.error_in_excel"))

        if result == 'bad_column_letter':
            session["show_error_notif"] = True
            session["excel_errors"] = [
                "Please review your input for column letters."]
            return redirect(url_for("student_routes.error_in_excel"))

        if isinstance(result[0], list):
            # Build error messages from structured errors
            excel_errors = []
            for problem in result:
                cell = f"{problem[2]}{problem[1]}"
                if problem[0] == "bad_format":
                    excel_errors.append(f"Bad data format in cell {cell}.")
                elif problem[0] == "duplicated_nc":
                    excel_errors.append(
                        f"Duplicated national code in cell {cell}.")
                elif problem[0] == 'unknown_class':
                    excel_errors.append(f"Unknown class name in cell {cell}.")
                else:
                    excel_errors.append(f"Unknown issue in cell {cell}.")

            session["show_error_notif"] = True
            session["excel_errors"] = excel_errors
            return redirect(url_for("student_routes.error_in_excel"))

        # Save ZIP file and extract student images
        zip_path = f"c:/sap-project/server/schools/{str(current_user.id)}/student_ref_images.zip"
        extracted_files_path = zip_path[:-4]
        zip_file.save(zip_path)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extracted_files_path)

        # Add validated students to database
        for student in result:
            class_id = Class.query.filter(
                Class.class_code == student['class']).first().id
            new_student = Student(
                student_name=student['name'],
                student_family=student['family'],
                student_national_code=student['national_code'],
                class_id=class_id,
                student_password=student['password'],
                school_id=current_user.id
            )

            db.session.add(new_student)
            db.session.flush()

            try:
                # Move image file to student's folder
                src = f"{extracted_files_path}/{reverse_class_code(student['class'])[1]}/{student['national_code']}.jpg"
                dst = f"c:/sap-project/server/schools/{str(current_user.id)}/{str(class_id)}/{str(new_student.student_national_code)}.jpg"
                shutil.move(src, dst)
            except FileNotFoundError:
                db.session.rollback()
                session["show_error_notif"] = True
                session["excel_errors"] = [
                    f"Cannot find image for student with national code '{student['national_code']}' in your ZIP file."
                ]
                return redirect(url_for("student_routes.error_in_excel"))

            db.session.commit()

            dm_create_student(
                school_id=str(current_user.id),
                class_id=str(class_id),
                student_code=str(new_student.student_national_code)
            )

        # Clean up
        shutil.rmtree(extracted_files_path)
        os.remove(zip_path)

        return redirect(url_for("student_routes.panel_students"))

    return render_template("student/add_from_excel.html")


@bp.route('/panel/students/edit_student/<student_national_code>', methods=['GET', 'POST'])
@login_required
def edit_student(student_national_code):
    """
    Edit a specific student's information.

    GET:
        - Display the edit form with the student's current data.

    POST:
        - Update student fields and save changes to the database.

    Returns:
        Redirect to student list or an error page.
    """
    school = School.query.filter(School.id == current_user.id).first()
    student = Student.query.filter(
        (Student.school_id == school.id) &
        (Student.student_national_code == student_national_code)
    ).first()

    old_student_code = student.student_national_code

    if not student:
        session["show_error_notif"] = True
        return redirect(url_for("student_routes.unknown_student_info"))

    if request.method == "POST":
        # Update student fields with form data
        student.student_name = request.form['student_name']
        student.student_family = request.form['student_family']
        student.student_national_code = request.form['student_national_code']
        student.student_password = request.form['student_password']

        try:
            db.session.commit()
            dm_edit_student(
                school_id=str(current_user.id),
                class_id=str(student.class_id),
                old_student_code=str(old_student_code),
                new_student_code=str(student.student_national_code)
            )
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
    Delete a student from the database and filesystem.

    Returns:
        Redirect to student list or error page if student not found.
    """
    school = School.query.filter(School.id == current_user.id).first()
    student = Student.query.filter(
        (Student.student_national_code == student_national_code) &
        (Student.school_id == school.id)
    ).first()

    if not student:
        session["show_error_notif"] = True
        return redirect(url_for("student_routes.unknown_student_info"))

    # Remove student directory and delete from database
    dm_delete_student(
        school_id=str(current_user.id),
        class_id=str(student.class_id),
        student_code=str(student.student_national_code)
    )
    db.session.delete(student)
    db.session.commit()

    return redirect(url_for('student_routes.panel_students'))


@bp.route('/panel/students/student_info/<student_national_code>')
@login_required
def student_info(student_national_code):
    """
    Display detailed information about a student.

    Returns:
        Rendered HTML page with student data or error page.
    """
    school = School.query.filter(School.id == current_user.id).first()
    student = Student.query.filter(
        (Student.student_national_code == student_national_code) &
        (Student.school_id == school.id)
    ).first()

    if not student:
        session["show_error_notif"] = True
        return redirect(url_for("student_routes.unknown_student_info"))

    return render_template('student/student_info.html', data=student)


@bp.route("/panel/students/unknown_student_info", methods=['GET', 'POST'])
@login_required
def unknown_student_info():
    """
    Render an error page when the student is not found in the system.

    Returns:
        Redirect to student panel if access is invalid.
        Rendered HTML error page otherwise.
    """
    if not session.pop('show_error_notif', False):
        return redirect(url_for('student_routes.panel_students'))

    return render_template('student/unknown_student_info.html')


@bp.route("/panel/students/duplicated_student_info", methods=['GET', 'POST'])
@login_required
def duplicated_student_info():
    """
    Render an error page when a duplicate student entry is detected.

    Returns:
        Redirect to add student form if access is invalid.
        Rendered HTML error page otherwise.
    """
    if not session.pop('show_error_notif', False):
        return redirect(url_for('student_routes.add_student'))

    return render_template('student/duplicated_student_info.html')


@bp.route("/panel/students/error_in_excel", methods=['GET', 'POST'])
@login_required
def error_in_excel():
    """
    Render an error page with validation issues from the uploaded Excel file.

    Returns:
        Redirect to Excel upload form if access is invalid.
        Rendered HTML error page otherwise.
    """
    if not session.pop('show_error_notif', False):
        return redirect(url_for('student_routes.add_from_excel'))

    errors = session.get("excel_errors", [])
    return render_template('student/error_in_excel.html', texts=errors)


@bp.route('/panel/students/file_permission_error')
@login_required
def file_permission_error():
    """
    Render an error page when the server cannot save the uploaded Excel file due to permission issues.

    Returns:
        Redirect to Excel upload form if access is invalid.
        Rendered HTML error page otherwise.
    """
    if not session.pop('show_error_notif', False):
        return redirect(url_for('student_routes.add_from_excel'))

    return render_template('student/file_permission_error.html')
