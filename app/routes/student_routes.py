# Import necessary modules
from app import db
from app.models._class import Class
from app.models.student import Student
from app.utils.generate_class_code import reverse_class_code
from app.server_side.directory_manager import create_student, edit_student, delete_student
from app.utils.excel_reading import add_students

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
            create_student(school_code=current_user.school_code, class_name=reverse_class_code(class_code)[1], student_national_code=student_national_code)
        except:
            # Rollback changes and redirect to an error page if unique constraints are violated
            db.session.rollback()
            return redirect(url_for('student_routes.go_to_duplicated_student_info'))

        # Redirect to the student list page after successful registration
        return redirect(url_for('student_routes.go_to_panel_students'))

    # Render the form for adding a new student
    classes = Class.query.filter(Class.school_code == current_user.school_code).all()
    return render_template('student/add_student.html', classes=classes)


@bp.route("/panel/students/add_from_excel", methods=['GET', 'POST'])
@login_required
def go_to_add_from_excel():
    if request.method == 'POST':
        classes = Class.query.filter(Class.school_code==current_user.school_code).all()
        classes_name = [class_.class_name for class_ in classes]

        students = Student.query.filter(Student.school_code==current_user.school_code).all()
        students_national_code = [student.student_national_code for student in students]

        file = request.files["file_input"]
        sheet_name = request.form["sheet"]
        name_letter = request.form["name"]
        family_letter = request.form["family"]
        nc_letter = request.form["national_code"]
        class_letter = request.form["class"]
        pass_letter = request.form["password"]

        file.save("students.xlsx")
        result = add_students('students.xlsx', sheet_name, name_letter, family_letter, nc_letter, class_letter, pass_letter, classes_name, students_national_code)
        

        if result == 'sheet_not_found': 
            text = "Please review your input for sheet name."
            return redirect(url_for("student_routes.go_to_error_in_excel", text=text))
        
        if result == 'bad_column_letter': 
            text = "Please review your input for column letters."
            return redirect(url_for("student_routes.go_to_error_in_excel", text=text))
        
        if isinstance(result, tuple):
            if result[0] == "bad_format":
                text = f"Please review the cell { result[2] }{ result[1] } because bad data format."
            elif result[0] == "duplicated_nc":
                text = f"Please review the cell { result[2] }{ result[1] } because duplicated value."
            elif result[0] == 'unknown_class':
                text = f"Please review the cell { result[2] }{ result[1] } because unknown class."
            else:
                text = f"Please review the cell { result[2] }{ result[1] } because unknown trouble."

            return redirect(url_for("student_routes.go_to_error_in_excel", text=text))

        for student in result:
            new_student = Student(student_name=student['name'],
                                  student_family=student['family'], 
                                  student_national_code=student['national_code'], 
                                  class_code=student['class'], 
                                  student_password=student['password'], 
                                  school_code=current_user.school_code)
            
            db.session.add(new_student)
        db.session.commit()
        
        return redirect(url_for("student_routes.go_to_panel_students"))
    else:
        return render_template("student/add_from_excel.html")


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

        # Find the student in the database
        student = Student.query.filter((Student.student_national_code == student_national_code) &
                                       (Student.school_code == current_user.school_code)).first()

        # Update the student's information
        student.student_name = new_name
        student.student_family = new_family
        student.student_national_code = new_national_code
        student.student_password = new_password

        try:
            # Commit the changes to the database
            db.session.commit()
            edit_student(school_code=current_user.school_code, class_name=reverse_class_code(student.class_code)[1], old_student_national_code=student_national_code, new_student_national_code=new_national_code)
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
    delete_student(school_code=current_user.school_code, class_name=reverse_class_code(student.class_code)[1], student_national_code=student_national_code)

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


@bp.route("/panel/students/error_in_excel/<text>", methods=['GET', 'POST'])
@login_required
def go_to_error_in_excel(text):
    return render_template('student/error_in_excel.html', text=text)