# Import necessary modules and components
from app import db
from app.models.models import Student, Teacher, Class
from app.utils.generate_class_code import generate_class_code
from app.utils.excel_reading import add_classes
from app.server_side.Website.directory_manager import (
    dm_create_class, dm_edit_class, dm_delete_class
)
from flask import Blueprint, redirect, render_template, request, url_for, session
from flask_login import current_user, login_required
import os

# Initialize Blueprint for class-related routes
bp = Blueprint('class_routes', __name__)


@bp.route('/panel/classes', methods=['GET', 'POST'])
@login_required
def panel_classes():
    """
    Displays the main panel for managing classes.
    Includes a search bar to filter classes by name or code.
    """
    # Retrieve search query from URL parameters
    query = request.args.get('q')
    if not query:
        # Show all classes for the current user's school if no search term is provided
        classes = Class.query.filter_by(
            school_code=current_user.school_code).all()
    else:
        # Filter classes by name or code using the search term
        classes = Class.query.filter(
            (Class.school_code == current_user.school_code) &
            ((Class.class_name.ilike(f'%{query}%')) | (
                Class.class_code.ilike(f'%{query}%')))
        ).all()

    # Render the class list page
    return render_template('class/classes.html', classes=classes)


@bp.route('/panel/classes/add_class', methods=['GET', 'POST'])
@login_required
def add_class():
    """
    Handles adding a new class.
    - GET: Renders the "Add Class" form.
    - POST: Processes form data, creates a new class, and redirects to the class list.
    """
    if request.method == 'POST':
        # Extract form data
        school_code = current_user.school_code
        class_name = request.form['class_name']
        class_code = generate_class_code(school_code, class_name)

        # Create a new Class object
        new_class = Class(
            class_name=class_name,
            class_code=class_code,
            school_code=school_code,
            teachers="[]"  # Initialize with no teachers
        )

        try:
            # Add class to the database and create its directory
            db.session.add(new_class)
            db.session.commit()
            dm_create_class(school_code=school_code, class_name=class_name)
        except Exception:
            # Handle duplicate class errors
            session["show_error_notif"] = True
            return redirect(url_for('class_routes.duplicated_class_info'))

        # Redirect to the class list after successful creation
        return redirect(url_for('class_routes.panel_classes'))

    # Render the "Add Class" form for GET requests
    return render_template('class/add_class.html')


@bp.route('/panel/classes/add_from_excel', methods=['GET', 'POST'])
@login_required
def add_from_excel():
    """
    Adds multiple classes from an Excel file.
    - GET: Renders the upload form.
    - POST: Processes the uploaded Excel file, validates data, and adds classes to the database.
    """
    if request.method == 'POST':
        global texts
        # Get existing class names to prevent duplicates
        classes = Class.query.filter_by(
            school_code=current_user.school_code).all()
        existing_class_names = [cls.class_name for cls in classes]

        # Retrieve uploaded file and form data
        file = request.files["file_input"]
        sheet_name = request.form["sheet"]
        name_letter = request.form["name"]

        excel_path = f"c:\\sap-project\\server\\schools\\{current_user.school_code}\\classes.xlsx"
        try:
            file.save(excel_path)
        except PermissionError:
            session["show_error_notif"] = True
            return redirect(url_for("class_routes.file_permission_error"))

        # Process the Excel file and validate format
        result = add_classes(excel_path, sheet_name,
                             name_letter, existing_class_names)
        os.remove(excel_path)

        # Handle known issues returned from the Excel parser
        if result == 'sheet_not_found':
            session["show_error_notif"] = True
            texts = ["Please review your input for the sheet name."]
            return redirect(url_for("class_routes.error_in_excel"))
        if result == 'bad_column_letter':
            session["show_error_notif"] = True
            texts = ["Please review your input for column letters."]
            return redirect(url_for("class_routes.error_in_excel"))

        # Handle data-specific errors in the Excel file
        if isinstance(result[0], list):
            texts = []
            for problem in result:
                cell = f"{problem[2]}{problem[1]}"
                if problem[0] == "bad_format":
                    texts.append(
                        f"Please review the cell {cell} because of bad data format.")
                elif problem[0] == "duplicated_name":
                    texts.append(
                        f"Please review the cell {cell} because of duplicated value.")
                else:
                    texts.append(
                        f"Please review the cell {cell} due to an unknown issue.")
            session["show_error_notif"] = True
            return redirect(url_for("class_routes.error_in_excel"))

        # Save successfully parsed class data to the database
        for cls in result:
            new_class = Class(
                class_name=cls['name'],
                class_code=cls['code'],
                school_code=current_user.school_code,
                teachers="[]"
            )
            db.session.add(new_class)
            dm_create_class(current_user.school_code, cls['name'])

        db.session.commit()
        return redirect(url_for('class_routes.panel_classes'))

    # Render the upload form for GET requests
    return render_template("class/add_from_excel.html")


@bp.route('/panel/classes/edit_class/<class_name>', methods=['GET', 'POST'])
@login_required
def edit_class(class_name):
    """
    Handles editing an existing class.
    Updates the class name, code, and related student/teacher references.
    """
    if request.method == "POST":
        # Generate new and old class codes
        new_name = request.form['class_name']
        new_code = generate_class_code(current_user.school_code, new_name)
        old_code = generate_class_code(current_user.school_code, class_name)

        # Fetch the class from the database
        cls = Class.query.filter_by(class_code=old_code).first()
        if cls is None:
            return redirect(url_for('class_routes.unknown_class_info'))

        # Update class details
        cls.class_code = new_code
        cls.class_name = new_name

        # Update all students in this class
        students = Student.query.filter_by(class_code=old_code).all()
        for student in students:
            student.class_code = new_code

        # Update class code in each teacher's class list
        teachers_national_codes = eval(cls.teachers)
        for national_code in teachers_national_codes:
            teacher = Teacher.query.filter_by(
                teacher_national_code=national_code).first()
            teacher_classes = eval(teacher.teacher_classes)
            index = teacher_classes.index(old_code)
            teacher_classes[index] = new_code
            teacher.teacher_classes = str(teacher_classes)

        try:
            # Commit changes and update the class directory
            db.session.commit()
            dm_edit_class(
                school_code=current_user.school_code,
                old_class_name=class_name,
                new_class_name=new_name
            )

            # Save the uploaded schedule file
            file = request.files['file-input']
            file.save(
                f'C:\\sap-project\\server\\schools\\{current_user.school_code}\\{new_name}\\schedule.xlsx')
        except Exception:
            session["show_error_notif"] = True
            return redirect(url_for('class_routes.duplicated_class_info'))

        return redirect(url_for('class_routes.panel_classes'))

    # Render the edit form for GET requests
    school_code = current_user.school_code
    class_code = generate_class_code(school_code, class_name)
    cls = Class.query.filter_by(class_code=class_code).first()
    if cls is None:
        session["show_error_notif"] = True
        return redirect(url_for('class_routes.unknown_class_info'))
    return render_template('class/edit_class.html', name=cls.class_name)


@bp.route('/panel/classes/remove/<class_name>', methods=['GET', 'POST'])
@login_required
def remove_class(class_name):
    """
    Removes a class and all associated data (students and teacher references).
    """
    # Generate class code and fetch class object
    class_code = generate_class_code(current_user.school_code, class_name)
    cls = Class.query.filter_by(class_code=class_code).first()

    if cls:
        # Delete all students in this class
        students = Student.query.filter_by(class_code=class_code).all()
        for student in students:
            db.session.delete(student)

        # Remove this class from each teacher's class list
        teachers_national_codes = eval(cls.teachers)
        for national_code in teachers_national_codes:
            teacher = Teacher.query.filter_by(
                teacher_national_code=national_code).first()
            teacher_classes = eval(teacher.teacher_classes)
            teacher_classes.remove(class_code)
            teacher.teacher_classes = str(teacher_classes)

        # Delete the class and commit changes
        db.session.delete(cls)
        db.session.commit()

        # Remove the class directory
        dm_delete_class(school_code=current_user.school_code,
                        class_name=class_name)

    return redirect(url_for('class_routes.panel_classes'))


@bp.route('/panel/classes/class_info/<class_name>')
@login_required
def class_info(class_name):
    """
    Displays detailed information about a specific class, including students and teachers.
    """
    class_code = generate_class_code(current_user.school_code, class_name)
    cls = Class.query.filter_by(class_code=class_code).first()

    if cls is None:
        session["show_error_notif"] = True
        return redirect(url_for('class_routes.unknown_class_info'))

    # Fetch teachers and students associated with the class
    teachers = [Teacher.query.filter_by(
        teacher_national_code=code).first() for code in eval(cls.teachers)]
    students = Student.query.filter_by(class_code=cls.class_code).all()

    return render_template('class/class_info.html', data=cls, teachers=teachers, students=students)


# Error pages for user feedback
@bp.route('/panel/classes/unknown_class_info')
@login_required
def unknown_class_info():
    """
    Displays an error page for unknown classes.
    """
    if not session.pop('show_error_notif', False):
        return redirect(url_for('class_routes.panel_classes'))
    return render_template('class/unknown_class_info.html')


@bp.route('/panel/classes/duplicated_class_info')
@login_required
def duplicated_class_info():
    """
    Displays an error page for duplicate class names/codes.
    """
    if not session.pop('show_error_notif', False):
        return redirect(url_for('class_routes.add_class'))
    return render_template('class/duplicated_class_info.html')


@bp.route("/panel/classes/error_in_excel", methods=['GET', 'POST'])
@login_required
def error_in_excel():
    """
    Displays an error page for Excel file parsing issues.
    Shows detailed feedback about which cells need correction.
    """
    if not session.pop('show_error_notif', False):
        return redirect(url_for('class_routes.add_from_excel'))
    return render_template('class/error_in_excel.html', texts=texts)


@bp.route('/panel/classes/file_permission_error')
@login_required
def file_permission_error():
    """
    Displays an error page for file saving permission issues.
    """
    if not session.pop('show_error_notif', False):
        return redirect(url_for('class_routes.add_from_excel'))
    return render_template('class/file_permission_error.html')
