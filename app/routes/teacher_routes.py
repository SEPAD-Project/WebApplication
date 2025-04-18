# Import necessary modules
from app import db
from app.models.models import Class, School, Teacher
from app.utils.generate_class_code import generate_class_code
from flask import Blueprint, redirect, render_template, request, url_for, session
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
    school = School.query.filter_by(
        school_code=current_user.school_code).first()
    teachers = school.teachers

    # Filter teachers based on the query (if provided)
    query = request.args.get('q')
    if query:
        teachers = [
            teacher for teacher in teachers
            if (query.lower() in teacher.teacher_name.lower() or query.lower() in teacher.teacher_national_code.lower())
        ]

    return render_template('teacher/teachers.html', teachers=teachers)


@bp.route('/panel/teachers/add_teacher', methods=['GET', 'POST'])
@login_required
def add_teacher():
    """
    Handles adding a new teacher to the school in the panel.
    - POST: Processes form data and adds the teacher to the database.
    - GET: Renders the form for adding a new teacher.
    """
    if request.method == 'POST':
        # Extract form data
        entry_national_code = request.form["teacher_national_code"]
        entry_password = request.form["teacher_password"]

        # Validate teacher existence and password
        teacher = Teacher.query.filter_by(
            teacher_national_code=entry_national_code).first()
        if not teacher:
            session["show_error_notif"] = True
            return redirect(url_for("teacher_routes.wrong_teacher_info"))
        if teacher.teacher_password != entry_password:
            session["show_error_notif"] = True
            return redirect(url_for("teacher_routes.wrong_teacher_info"))

        # Add selected classes to the teacher's class list
        selected_classes = request.form.getlist("selected_classes")

        if selected_classes:
            school = School.query.filter_by(
                school_code=current_user.school_code).first()
            school.teachers.append(teacher)

        for class_code in selected_classes:
            class_ = Class.query.filter_by(class_code=class_code).first()
            if teacher not in class_.teachers:
                class_.teachers.append(teacher)

        db.session.commit()

        return redirect(url_for("teacher_routes.panel_teachers"))

    # Render the form with available classes
    school = School.query.filter_by(
        school_code=current_user.school_code).first()
    return render_template("teacher/add_teacher.html", classes=school.classes)


@bp.route("/panel/teachers/remove_teacher/<teacher_national_code>", methods=['POST', 'GET'])
@login_required
def remove_teacher(teacher_national_code):
    """
    Handles removing a teacher from the school in the panel.
    - Removes the teacher from all associated classes and the school's teacher list.
    """
    school = School.query.filter_by(
        school_code=current_user.school_code).first()
    teacher = Teacher.query.filter_by(
        teacher_national_code=teacher_national_code).first()
    if not teacher or not teacher in school.teachers:
        session["show_error_notif"] = True
        return redirect(url_for('teacher_routes.wrong_teacher_info'))

    school = School.query.filter_by(
        school_code=current_user.school_code).first()

    for class_ in school.classes:
        if teacher in class_.teachers:
            class_.teachers.remove(teacher)

    school.teachers.remove(teacher)

    db.session.commit()
    return redirect(url_for('teacher_routes.panel_teachers'))


@bp.route('/panel/teachers/edit_teacher/<teacher_national_code>', methods=['GET', 'POST'])
@login_required
def edit_teacher(teacher_national_code):
    """
    Handles editing an existing teacher in the panel.
    - POST: Updates the teacher's class assignments.
    - GET: Renders the form for editing the teacher.
    """
    school = School.query.filter_by(
        school_code=current_user.school_code).first()
    teacher = Teacher.query.filter_by(
        teacher_national_code=teacher_national_code).first()
    if not teacher or not teacher in school.teachers:
        session["show_error_notif"] = True
        return redirect(url_for('teacher_routes.wrong_teacher_info'))

    if request.method == 'POST':
        # Update the teacher's class assignments
        new_classes = request.form.getlist('selected_classes')

        for class_ in school.classes:
            if teacher in class_.teachers:
                class_.teachers.remove(teacher)

        # Add the teacher to the new classes
        for class_code in new_classes:
            class_ = Class.query.filter_by(class_code=class_code).first()
            class_.teachers.append(teacher)

        db.session.commit()
        return redirect(url_for('teacher_routes.panel_teachers'))

    # Render the form with available classes
    return render_template("teacher/edit_teacher.html", classes=school.classes, teacher=teacher)


@bp.route("/panel/teachers/teacher_info/<teacher_national_code>")
@login_required
def teacher_info(teacher_national_code):
    """
    Displays detailed information about a specific teacher.
    """
    school = School.query.filter_by(
        school_code=current_user.school_code).first()
    teacher = Teacher.query.filter_by(
        teacher_national_code=teacher_national_code).first()

    if not teacher in school.teachers:
        session["show_error_notif"] = True
        return redirect(url_for('teacher_routes.wrong_teacher_info'))

    return render_template('teacher/teacher_info.html', data=teacher)


@bp.route('/panel/teachers/wrong_teacher_info', methods=['GET', 'POST'])
@login_required
def wrong_teacher_info():
    """
    Displays an error page for invalid teacher information.
    """
    if not session.pop('show_error_notif', False):
        return redirect(url_for('teacher_routes.add_teacher'))
    return render_template("teacher/wrong_teacher_info.html")
