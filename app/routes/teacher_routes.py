# Import necessary modules
from app import db
from app.models._class import Class
from app.models.school import School
from app.models.teacher import Teacher
from app.utils.generate_class_code import generate_class_code

from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required

# Initialize the Blueprint for teacher-related routes
bp = Blueprint('teacher_routes', __name__)


@bp.route('/panel/teachers')
@login_required
def panel_teachers():
    """
    Displays the list of teachers in the panel.
    - Filters teachers by name or national code if a query is provided.
    - Shows all teachers if no query is provided.
    """
    # Retrieve the school object and its associated teachers
    school = School.query.filter(School.school_code == current_user.school_code).first()
    teachers = []
    for national_code in eval(school.teachers):
        teacher = Teacher.query.filter(Teacher.teacher_national_code == national_code).first()
        if teacher:
            teachers.append(teacher)

    # Filter teachers by name or national code based on the query
    query = request.args.get('q')
    if query:
        filtered_teachers = [
            teacher for teacher in teachers
            if (query.lower() in teacher.teacher_name.lower() or query.lower() in teacher.teacher_national_code.lower())
        ]
        teachers = filtered_teachers

    # Render the HTML page displaying the list of teachers
    return render_template('teacher/teachers.html', teachers=teachers)


@bp.route('/panel/teachers/add_teacher', methods=['GET', 'POST'])
@login_required
def add_teacher():
    """
    Handles adding a new teacher to the school in the panel.
    - For POST requests, processes form data and adds the teacher to the database.
    - For GET requests, renders the form for adding a new teacher.
    """
    if request.method == 'POST':
        # Retrieve form data
        entry_national_code = request.form["teacher_national_code"]
        entry_password = request.form["teacher_password"]

        # Find the teacher in the database
        teacher = Teacher.query.filter(Teacher.teacher_national_code == entry_national_code).first()

        if teacher is None:
            # Redirect to an error page if the teacher does not exist
            return redirect(url_for("teacher_routes.wrong_teacher_info"))

        # Verify the teacher's password
        if teacher.teacher_password == entry_password:
            # Get the selected classes from the form
            classes = request.form.getlist("selected_classes")

            if classes:
                # Add the teacher's national code to the school's teacher list
                school = School.query.filter(School.school_code == current_user.school_code).first()
                teachers = eval(school.teachers)
                teachers.append(teacher.teacher_national_code)
                school.teachers = str(teachers)

            for class_code in classes:
                # Add the class code to the teacher's class list
                teacher_classes = eval(teacher.teacher_classes)
                teacher_classes.append(class_code)
                teacher.teacher_classes = str(teacher_classes)

                # Add the teacher's national code to the class's teacher list
                class_ = Class.query.filter(Class.class_code == class_code).first()
                class_teachers = eval(class_.teachers)
                class_teachers.append(entry_national_code)
                class_.teachers = str(class_teachers)

            # Commit changes to the database
            db.session.commit()
            return redirect(url_for("teacher_routes.panel_teachers"))
        else:
            # Redirect to an error page if the password is incorrect
            return redirect(url_for("teacher_routes.wrong_teacher_info"))

    # Render the form for adding a new teacher
    school_classes = Class.query.filter(Class.school_code == current_user.school_code).all()
    return render_template("teacher/add_teacher.html", classes=school_classes)


@bp.route("/panel/students/remove_teacher/<teacher_national_code>", methods=['POST', 'GET'])
@login_required
def remove_teacher(teacher_national_code):
    """
    Handles removing a teacher from the school in the panel.
    - Removes the teacher from all associated classes and the school's teacher list.
    """
    # Remove the teacher's classes
    teacher = Teacher.query.filter(Teacher.teacher_national_code == teacher_national_code).first()
    school_code = generate_class_code(current_user.school_code, '')
    teacher_classes = eval(teacher.teacher_classes)
    for class_code in teacher_classes:
        if class_code[:3] == school_code:
            teacher_classes.remove(class_code)
    teacher.teacher_classes = str(teacher_classes)

    # Remove the teacher from each class's teacher list
    classes = Class.query.filter(Class.school_code == current_user.school_code).all()
    for class_ in classes:
        teachers = eval(class_.teachers)
        try:
            teachers.remove(teacher_national_code)
        except ValueError:
            continue
        class_.teachers = str(teachers)

    # Remove the teacher from the school's teacher list
    school = School.query.filter(School.school_code == current_user.school_code).first()
    school_teachers = eval(school.teachers)
    school_teachers.remove(teacher_national_code)
    school.teachers = str(school_teachers)

    # Commit changes to the database
    db.session.commit()

    # Redirect to the teacher list page
    return redirect(url_for('teacher_routes.panel_teachers'))


@bp.route('/panel/edit_teacher/<teacher_national_code>', methods=['GET', 'POST'])
@login_required
def edit_teacher(teacher_national_code):
    """
    Handles editing an existing teacher in the panel.
    - For POST requests, updates the teacher's class assignments.
    - For GET requests, renders the form for editing the teacher.
    """
    if request.method == 'POST':
        # Find the teacher in the database
        teacher = Teacher.query.filter(Teacher.teacher_national_code == teacher_national_code).first()
        if teacher is None:
            return redirect(url_for('teacher_routes.wrong_teacher_info'))

        # Retrieve the new class assignments from the form
        new_classes = request.form.getlist('selected_classes')
        teacher_classes = eval(teacher.teacher_classes)
        school_code = generate_class_code(current_user.school_code, '')

        # Remove the teacher from all previous classes
        for class_code in teacher_classes:
            if class_code[:3] == school_code:
                class_ = Class.query.filter(Class.class_code == class_code).first()
                class_teachers = eval(class_.teachers)
                class_teachers.remove(teacher_national_code)
                class_.teachers = str(class_teachers)

        # Add the teacher to the new classes
        for class_code in new_classes:
            class_ = Class.query.filter(Class.class_code == class_code).first()
            class_teachers = eval(class_.teachers)
            class_teachers.append(teacher_national_code)
            class_.teachers = str(class_teachers)

        # Update the teacher's class list
        teacher_classes.clear()
        for class_code in new_classes:
            teacher_classes.append(class_code)
        teacher.teacher_classes = str(teacher_classes)

        # Commit changes to the database
        db.session.commit()

        # Redirect to the teacher list page
        return redirect(url_for('teacher_routes.panel_teachers'))

    # Render the form for editing the teacher
    teacher = Teacher.query.filter(Teacher.teacher_national_code == teacher_national_code).first()
    if teacher is None:
        return redirect(url_for('teacher_routes.wrong_teacher_info'))

    classes = Class.query.filter(Class.school_code == current_user.school_code).all()
    return render_template("teacher/edit_teacher.html", classes=classes, teacher=teacher)


@bp.route("/panel/teachers/teacher_info/<teacher_national_code>")
@login_required
def teacher_info(teacher_national_code):
    """
    Displays detailed information about a specific teacher.
    """
    # Find the school and teacher objects
    school = School.query.filter(School.school_code == current_user.school_code).first()
    teacher = Teacher.query.filter(Teacher.teacher_national_code == teacher_national_code).first()

    if teacher is None:
        # Redirect to an error page if the teacher does not exist
        return redirect(url_for('teacher_routes.wrong_teacher_info'))

    if teacher.teacher_national_code in eval(school.teachers):
        # Render the teacher info page if the teacher belongs to the school
        return render_template('teacher/teacher_info.html', data=teacher)
    else:
        # Redirect to an error page if the teacher does not belong to the school
        return redirect(url_for('teacher_routes.wrong_teacher_info'))


@bp.route('/panel/wrong_teacher_info', methods=['GET', 'POST'])
@login_required
def wrong_teacher_info():
    """
    Displays an error page for invalid teacher information.
    """
    return render_template("teacher/wrong_teacher_info.html")