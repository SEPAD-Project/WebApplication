# Import necessary modules and components
from app import db

from app.models._class import Class
from app.models.student import Student
from app.models.teacher import Teacher
from app.utils.generate_class_code import generate_class_code
from app.utils.excel_reading import add_classes
from app.server_side.Website.directory_manager import dm_create_class, dm_edit_class, dm_delete_class

from flask import Blueprint, redirect, render_template, request, url_for, session
from flask_login import current_user, login_required

import os

# Initialize Blueprint for class-related routes
bp = Blueprint('class_routes', __name__)


@bp.route('/panel/classes', methods=['GET', 'POST'])
@login_required
def panel_classes():
    """
    Show the main panel for managing classes.
    Includes a search bar to filter classes by name or code.
    """
    # Get search query from URL parameters
    query = request.args.get('q')

    if query == "" or query is None:
        # Show all classes for the current user's school if no search term
        classes = Class.query.filter(
            Class.school_code == current_user.school_code).all()
    else:
        # Filter classes by name or code using the search term
        classes = Class.query.filter(
            (Class.school_code == current_user.school_code) &
            ((Class.class_name.ilike(f'%{query}%')) |
             (Class.class_code.ilike(f'%{query}%')))
        ).all()

    # Render class list page
    return render_template('class/classes.html', classes=classes)


@bp.route('/panel/classes/add_class', methods=['GET', 'POST'])
@login_required
def add_class():
    """
    Handle the add class operation.
    """
    if request.method == 'POST':
        # Get the current user's school code and form data
        school_code = current_user.school_code
        class_name = request.form['class_name']

        # Generate a unique class code based on name and school
        class_code = generate_class_code(school_code, class_name)

        # Initially, there are no teachers assigned to the class
        teachers = "[]"

        # Create new Class object
        new_class = Class(class_name, class_code, school_code, teachers)

        try:
            # Add class to database and create class directory
            db.session.add(new_class)
            db.session.commit()
            dm_create_class(school_code=school_code, class_name=class_name)
        except:
            # Class already exists (based on name), show error
            session["show_error_notif"] = True
            return redirect(url_for('class_routes.duplicated_class_info'))

        # Redirect back to class list after successful creation
        return redirect(url_for('class_routes.panel_classes'))

    # If GET request, show the "Add Class" form
    return render_template('class/add_class.html')


@bp.route('/panel/classes/add_from_excel', methods=['GET', 'POST'])
@login_required
def add_from_excel():
    """
    Add multiple classes from an Excel file.
    """
    if request.method == 'POST':
        global texts

        # Get existing class names to prevent duplicates
        classes = Class.query.filter(Class.school_code == current_user.school_code).all()
        classes_name = [class_.class_name for class_ in classes]

        # Retrieve uploaded file and form data
        file = request.files["file_input"]
        sheet_name = request.form["sheet"]
        name_letter = request.form["name"]
        
        excel_path = f"c:\sap-project\server\schools\{current_user.school_code}\classes.xlsx"
        try:
            file.save(excel_path)
        except PermissionError:
            session["show_error_notif"] = True
            return redirect(url_for("class_routes.file_permission_error"))
        
        # Process Excel file and validate format
        result = add_classes(excel_path, sheet_name, name_letter, classes_name)

        os.remove(excel_path)

        # Handle known issues returned from Excel parser
        if result == 'sheet_not_found': 
            session["show_error_notif"] = True
            texts = ["Please review your input for sheet name."]
            return redirect(url_for("class_routes.error_in_excel"))

        if result == 'bad_column_letter': 
            session["show_error_notif"] = True
            texts= ["Please review your input for column letters."]
            return redirect(url_for("class_routes.error_in_excel"))

        # Handle data-specific errors in the Excel file
        if isinstance(result[0], list):
            texts = []
            for problem in result:
                cell = f"{problem[2]}{problem[1]}"
                if problem[0] == "bad_format":
                    texts.append(f"Please review the cell {cell} because of bad data format.")
                elif problem[0] == "duplicated_name":
                    texts.append(f"Please review the cell {cell} because of duplicated value.")
                else:
                    texts.append(f"Please review the cell {cell} due to an unknown issue.")

            session["show_error_notif"] = True
            return redirect(url_for("class_routes.error_in_excel"))

        # Save successfully parsed class data to the database
        for class_ in result:
            new_class = Class(class_name=class_['name'], class_code=class_['code'], school_code=current_user.school_code, teachers='[]')
            db.session.add(new_class)
            dm_create_class(current_user.school_code, class_['name'])

        db.session.commit()
        return redirect(url_for('class_routes.panel_classes'))

    # GET: Show upload form
    return render_template("class/add_from_excel.html")


@bp.route('/panel/classes/edit_class/<class_name>', methods=['GET', 'POST'])
@login_required
def edit_class(class_name):
    """
    Handle class editing.
    Changes the name and code of the class and updates all related students and teachers.
    """
    if request.method == "POST":
        # Get new name and generate updated class code
        new_name = request.form['class_name']
        new_code = generate_class_code(current_user.school_code, new_name)
        old_code = generate_class_code(current_user.school_code, class_name)

        # Get the class from database
        class_ = Class.query.filter(Class.class_code == old_code).first()

        # If class not found, possibly tampered data
        if class_ is None:
            return redirect(url_for('class_routes.unknown_class_info'))

        # Update class details
        class_.class_code = new_code
        class_.class_name = new_name

        # Update all students of this class with new code
        students = Student.query.filter(Student.class_code == old_code).all()
        for student in students:
            student.class_code = new_code

        # Update class code in every teacher's class list
        teachers_national_code = eval(class_.teachers)
        for national_code in teachers_national_code:
            teacher = Teacher.query.filter(Teacher.teacher_national_code == national_code).first()
            teacher_classes = eval(teacher.teacher_classes)
            index = teacher_classes.index(old_code)
            teacher_classes[index] = new_code
            teacher.teacher_classes = str(teacher_classes)

        try:
            db.session.commit()
            dm_edit_class(school_code=current_user.school_code, old_class_name=class_name, new_class_name=new_name)

            file = request.files['file-input']
            file.save(f'C:\sap-project\server\schools\{school_code}\{new_name}\schedule.xlsx')
        except:
            session["show_error_notif"] = True
            return redirect(url_for('class_routes.duplicated_class_info'))

        return redirect(url_for('class_routes.panel_classes'))

    # GET: Show edit form with existing class name
    school_code = current_user.school_code
    class_code = generate_class_code(school_code, class_name)
    class_ = Class.query.filter(Class.class_code == class_code).first()

    if class_ is None:
        session["show_error_notif"] = True
        return redirect(url_for('class_routes.unknown_class_info'))

    return render_template('class/edit_class.html', name=class_.class_name)


@bp.route('/panel/classes/remove/<class_name>', methods=['GET', 'POST'])
@login_required
def remove_class(class_name):
    """
    Remove a class and all its associated data (students and teacher references).
    """
    # Generate class code and fetch class object
    class_code = generate_class_code(current_user.school_code, class_name)
    class_ = Class.query.filter(Class.class_code == class_code).first()

    # Delete the class
    db.session.delete(class_)

    # Remove all students in this class
    students = Student.query.filter(Student.class_code == class_code).all()
    for student in students:
        db.session.delete(student)

    # Remove this class from each teacher's class list
    teachers_national_code = eval(class_.teachers)
    for national_code in teachers_national_code:
        teacher = Teacher.query.filter(Teacher.teacher_national_code == national_code).first()
        teacher_classes = eval(teacher.teacher_classes)
        teacher_classes.remove(class_code)
        teacher.teacher_classes = str(teacher_classes)

    # Commit all deletions and remove related directory
    db.session.commit()
    dm_delete_class(school_code=current_user.school_code, class_name=class_name)

    return redirect(url_for('class_routes.panel_classes'))


@bp.route('/panel/classes/class_info/<class_name>')
@login_required
def class_info(class_name):
    """
    Show detailed info about a specific class including its students and teachers.
    """
    class_code = generate_class_code(current_user.school_code, class_name)
    class_ = Class.query.filter(Class.class_code == class_code).first()

    if class_ is None:
        session["show_error_notif"] = True
        return redirect(url_for('class_routes.unknown_class_info'))

    teachers = [Teacher.query.filter(Teacher.teacher_national_code == code).first()
                for code in eval(class_.teachers)]
    students = Student.query.filter(Student.class_code == class_.class_code).all()

    return render_template('class/class_info.html', data=class_, teachers=teachers, students=students)


# Error pages for user feedback

@bp.route('/panel/classes/unknown_class_info')
@login_required
def unknown_class_info():
    """
    Error page for unknown class (e.g., edited or deleted manually).
    """
    if not session.get('show_error_notif', False):
        return redirect(url_for('class_routes.panel_classes'))
    session.pop('show_error_notif', None)
    return render_template('class/unknown_class_info.html')


@bp.route('/panel/classes/duplicated_class_info')
@login_required
def duplicated_class_info():
    """
    Error page for class name/code duplication.
    """
    if not session.get('show_error_notif', False):
        return redirect(url_for('class_routes.add_class'))
    session.pop('show_error_notif', None)
    return render_template('class/duplicated_class_info.html')


@bp.route("/panel/classes/error_in_excel", methods=['GET', 'POST'])
@login_required
def error_in_excel():
    """
    Error page for Excel file parsing issues.
    Shows detailed info about which cells need correction.
    """
    if not session.get('show_error_notif', False):
        return redirect(url_for('class_routes.add_from_excel'))
    session.pop('show_error_notif', None)
    return render_template('class/error_in_excel.html', texts=texts)


@bp.route('/panel/classes/file_permission_error')
@login_required
def file_permission_error():
    """
    Error page for file saving permission issues (Windows-only mostly).
    """
    if not session.get('show_error_notif', False):
        return redirect(url_for('class_routes.add_from_excel'))
    session.pop('show_error_notif', None)
    return render_template('class/file_permission_error.html')
