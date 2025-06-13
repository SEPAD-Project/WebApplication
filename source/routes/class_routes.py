# Standard Library Imports
import os

# Third-party Imports
from flask import Blueprint, redirect, render_template, request, url_for, session
from flask_login import current_user, login_required

# Local Application Imports
from source import db
from source.models.models import Student, Teacher, Class, School
from source.utils.generate_class_code import generate_class_code
from source.utils.excel_reading import add_classes, schedule_checking
from source.server_side.Website.directory_manager import dm_create_class, dm_delete_class

# Initialize Blueprint for class-related routes
bp = Blueprint('class_routes', __name__)


@bp.route('/panel/classes', methods=['GET', 'POST'])
@login_required
def panel_classes():
    """
    Display the main panel for managing classes with optional search functionality.

    GET:
        - Show all classes or filter them by search query.
    POST:
        - Not used in this route.
    """
    query = request.args.get('q')
    school = School.query.filter(School.id == current_user.id).first()

    if not query:
        # Show all classes if no search query is provided
        classes = school.classes
    else:
        # Filter classes by class name or class code
        classes = Class.query.filter(
            (Class.school_id == current_user.id) &
            ((Class.class_name.ilike(f'%{query}%')) | (Class.class_code.ilike(f'%{query}%')))
        ).all()

    return render_template('class/classes.html', classes=classes)


@bp.route('/panel/classes/add_class', methods=['GET', 'POST'])
@login_required
def add_class():
    """
    Handle the process of adding a new class.

    GET:
        - Render the 'Add Class' form.

    POST:
        - Process form data, create a new class, and redirect to the class list.
    """
    if request.method == 'POST':
        # Extract class name from form
        class_name = request.form['class_name']
        class_code = generate_class_code(current_user.school_code, class_name)
        school_id = current_user.id

        # Create a new Class instance
        new_class = Class(
            class_name=class_name,
            class_code=class_code,
            school_id=school_id,
        )

        try:
            # Add and flush the new class to the database and create its directory
            db.session.add(new_class)
            db.session.flush(new_class)

            dm_create_class(school_id=str(school_id), class_id=str(new_class.id))
           
            # Commit changes to database 
            db.session.commit()
        except Exception:
            # Handle possible database errors (e.g., duplicate entry)
            session["show_error_notif"] = True
            return redirect(url_for('class_routes.duplicated_class_info'))

        return redirect(url_for('class_routes.panel_classes'))

    return render_template('class/add_class.html')


@bp.route('/panel/classes/add_from_excel', methods=['GET', 'POST'])
@login_required
def add_from_excel():
    """
    Handle the process of adding multiple classes from an uploaded Excel file.

    GET:
        - Render the Excel upload form.

    POST:
        - Process the uploaded Excel file and add classes.
    """
    if request.method == 'POST':
        # Retrieve existing classes to check for duplicates
        classes = Class.query.filter(Class.school_id == current_user.id).all()
        existing_class_names = [cls.class_name for cls in classes]

        # Retrieve uploaded file and form inputs
        file = request.files["file_input"]
        sheet_name = request.form["sheet"]
        name_letter = request.form["name"]

        # Define file save path
        excel_path = f"c:\\sap-project\\server\\schools\\{str(current_user.id)}\\classes.xlsx"

        try:
            # Save the uploaded file
            file.save(excel_path)
        except PermissionError:
            # Handle file save permission issues
            session["show_error_notif"] = True
            return redirect(url_for("class_routes.file_permission_error"))

        # Process the Excel file
        result = add_classes(excel_path, sheet_name, name_letter, existing_class_names)

        # Delete the uploaded file after processing
        os.remove(excel_path)

        # Handle known errors returned by Excel processing
        if result == 'sheet_not_found':
            session["show_error_notif"] = True
            session["excel_errors"] = ["Please review your input for the sheet name."]
            return redirect(url_for("class_routes.error_in_excel"))

        if result == 'bad_column_letter':
            session["show_error_notif"] = True
            session["excel_errors"] = ["Please review your input for column letters."]
            return redirect(url_for("class_routes.error_in_excel"))

        if isinstance(result[0], list):
            # Collect detailed Excel data errors
            excel_errors = []
            for problem in result:
                cell = f"{problem[2]}{problem[1]}"
                if problem[0] == "bad_format":
                    excel_errors.append(f"Bad data format in cell {cell}.")
                elif problem[0] == "duplicated_name":
                    excel_errors.append(f"Duplicated value in cell {cell}.")
                else:
                    excel_errors.append(f"Unknown issue in cell {cell}.")

            session["show_error_notif"] = True
            session["excel_errors"] = excel_errors
            return redirect(url_for("class_routes.error_in_excel"))

        # If no errors, add classes to the database
        for cls in result:
            new_class = Class(
                class_name=cls['name'],
                class_code=cls['code'],
                school_id=current_user.id,
            )
            db.session.add(new_class)
            db.session.commit()
            
            dm_create_class(str(current_user.id), str(new_class.id))

        return redirect(url_for('class_routes.panel_classes'))

    return render_template("class/add_from_excel.html")


@bp.route('/panel/classes/edit_class/<class_name>', methods=['GET', 'POST'])
@login_required
def edit_class(class_name):
    """
    Handle editing an existing class.

    GET:
        - Render the class edit form.

    POST:
        - Update class name and class code.
        - Save uploaded schedule file if provided.
    """
    if request.method == "POST":
        # Extract new class name from form
        new_name = request.form['class_name']
        new_code = generate_class_code(current_user.school_code, new_name)
        old_code = generate_class_code(current_user.school_code, class_name)

        # Fetch the current class from the database
        cls = Class.query.filter(Class.class_code == old_code).first()
        if cls is None:
            session["show_error_notif"] = True
            return redirect(url_for('class_routes.unknown_class_info'))

        # Update class name and code
        cls.class_name = new_name
        cls.class_code = new_code

        # Handle uploaded schedule file
        file = request.files.get('file-input')
        if file:
            file_path = f'C:\\sap-project\\server\\schools\\{str(current_user.id)}\\{str(cls.id)}\\schedule.xlsx'
            file.save(file_path)
        
        problems = schedule_checking(file_path, 'Sheet1', [teacher.teacher_national_code for teacher in cls.teachers])
        if not (problems == []):
            print(problems)
            os.remove(file_path)
            session["show_error_notif"] = True
            session["schedule_errors"] = problems
            return redirect(url_for("class_routes.error_in_schedule")) 

        try:
            db.session.commit()
        except Exception:
            session["show_error_notif"] = True
            return redirect(url_for('class_routes.duplicated_class_info'))

        return redirect(url_for('class_routes.panel_classes'))

    # Handle GET request: Render the edit form
    class_code = generate_class_code(current_user.school_code, class_name)
    cls = Class.query.filter(Class.class_code == class_code).first()
    if cls is None:
        session["show_error_notif"] = True
        return redirect(url_for('class_routes.unknown_class_info'))

    return render_template('class/edit_class.html', name=cls.class_name)


@bp.route('/panel/classes/remove/<class_name>', methods=['GET', 'POST'])
@login_required
def remove_class(class_name):
    """
    Remove a class along with all associated data (students, teachers).

    GET/POST:
        - Delete the class record.
        - Remove the corresponding directory.
    """
    # Generate class code and fetch the class
    class_code = generate_class_code(current_user.school_code, class_name)
    cls = Class.query.filter(Class.class_code == class_code).first()

    if cls:
        db.session.delete(cls)
        db.session.commit()
        dm_delete_class(school_id=str(current_user.id), class_id=str(cls.id))

    return redirect(url_for('class_routes.panel_classes'))


@bp.route('/panel/classes/class_info/<class_name>')
@login_required
def class_info(class_name):
    """
    Display detailed information about a specific class, including students and teachers.
    """
    # Generate class code and fetch the class
    class_code = generate_class_code(current_user.school_code, class_name)
    cls = Class.query.filter(Class.class_code == class_code).first()

    if cls is None:
        session["show_error_notif"] = True
        return redirect(url_for('class_routes.unknown_class_info'))

    teachers = cls.teachers
    students = cls.students

    return render_template('class/class_info.html', data=cls, teachers=teachers, students=students)


@bp.route('/panel/classes/unknown_class_info')
@login_required
def unknown_class_info():
    """
    Display an error page when the specified class is not found.
    """
    if not session.pop('show_error_notif', False):
        return redirect(url_for('class_routes.panel_classes'))

    return render_template('class/unknown_class_info.html')


@bp.route('/panel/classes/duplicated_class_info')
@login_required
def duplicated_class_info():
    """
    Display an error page when a class name or code conflict occurs.
    """
    if not session.pop('show_error_notif', False):
        return redirect(url_for('class_routes.add_class'))

    return render_template('class/duplicated_class_info.html')


@bp.route("/panel/classes/error_in_excel", methods=['GET', 'POST'])
@login_required
def error_in_excel():
    """
    Display detailed feedback for Excel file parsing errors.
    """
    if not session.pop('show_error_notif', False):
        return redirect(url_for('class_routes.add_from_excel'))

    # Retrieve error messages stored in session
    excel_errors = session.get("excel_errors", [])

    return render_template('class/error_in_excel.html', texts=excel_errors)


@bp.route("/panel/classes/error_in_schedule", methods=['GET', 'POST'])
@login_required
def error_in_schedule():
    """
    Display detailed feedback for Schedule Excel file parsing errors.
    """
    if not session.pop('show_error_notif', False):
        return redirect(url_for('class_routes.edit_class'))

    # Retrieve error messages stored in session
    schedule_errors = session.get("schedule_errors", [])

    return render_template('class/error_in_excel.html', texts=schedule_errors)


@bp.route('/panel/classes/file_permission_error')
@login_required
def file_permission_error():
    """
    Display an error page for file saving permission issues.
    """
    if not session.pop('show_error_notif', False):
        return redirect(url_for('class_routes.add_from_excel'))

    return render_template('class/file_permission_error.html')
