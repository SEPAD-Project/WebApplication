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
    if not school:
        return redirect(url_for("teacher_routes.wrong_teacher_info"))

    # Retrieve teachers from the school's teacher list
    teachers = []
    for national_code in eval(school.teachers):
        teacher = Teacher.query.filter_by(
            teacher_national_code=national_code).first()
        if teacher:
            teachers.append(teacher)

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
            teachers = eval(school.teachers)
            teachers.append(teacher.teacher_national_code)
            school.teachers = str(teachers)

            for class_code in selected_classes:
                # Add the class code to the teacher's class list
                teacher_classes = eval(teacher.teacher_classes)
                teacher_classes.append(class_code)
                teacher.teacher_classes = str(teacher_classes)

                # Add the teacher's national code to the class's teacher list
                class_ = Class.query.filter_by(class_code=class_code).first()
                class_teachers = eval(class_.teachers)
                class_teachers.append(entry_national_code)
                class_.teachers = str(class_teachers)

            db.session.commit()

        return redirect(url_for("teacher_routes.panel_teachers"))

    # Render the form with available classes
    school_classes = Class.query.filter_by(
        school_code=current_user.school_code).all()
    return render_template("teacher/add_teacher.html", classes=school_classes)


@bp.route("/panel/teachers/remove_teacher/<teacher_national_code>", methods=['POST', 'GET'])
@login_required
def remove_teacher(teacher_national_code):
    """
    Handles removing a teacher from the school in the panel.
    - Removes the teacher from all associated classes and the school's teacher list.
    """
    teacher = Teacher.query.filter_by(
        teacher_national_code=teacher_national_code).first()
    if not teacher:
        session["show_error_notif"] = True
        return redirect(url_for('teacher_routes.wrong_teacher_info'))

    school = School.query.filter_by(
        school_code=current_user.school_code).first()
    teachers = eval(school.teachers)

    # Ensure the teacher is in the school's list
    if teacher.teacher_national_code not in teachers:
        session["show_error_notif"] = True
        return redirect(url_for('teacher_routes.wrong_teacher_info'))

    # Remove the teacher's classes
    school_code = generate_class_code(current_user.school_code, '')
    teacher_classes = eval(teacher.teacher_classes)
    for class_code in teacher_classes:
        if class_code.startswith(school_code):
            teacher_classes.remove(class_code)

    teacher.teacher_classes = str(teacher_classes)

    # Remove the teacher from each class's teacher list
    classes = Class.query.filter_by(school_code=current_user.school_code).all()
    for class_ in classes:
        teachers = eval(class_.teachers)
        try:
            teachers.remove(teacher_national_code)
        except ValueError:
            continue
        class_.teachers = str(teachers)

    # Remove the teacher from the school's teacher list
    school_teachers = eval(school.teachers)
    school_teachers.remove(teacher.teacher_national_code)
    school.teachers = str(school_teachers)

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
    teacher = Teacher.query.filter_by(
        teacher_national_code=teacher_national_code).first()
    if not teacher:
        session["show_error_notif"] = True
        return redirect(url_for('teacher_routes.wrong_teacher_info'))

    school = School.query.filter_by(
        school_code=current_user.school_code).first()
    teachers = eval(school.teachers)

    # Ensure the teacher is in the school's list
    if teacher.teacher_national_code not in teachers:
        session["show_error_notif"] = True
        return redirect(url_for('teacher_routes.wrong_teacher_info'))

    if request.method == 'POST':
        # Update the teacher's class assignments
        new_classes = request.form.getlist('selected_classes')
        teacher_classes = eval(teacher.teacher_classes)
        school_code = generate_class_code(current_user.school_code, '')

        # Remove the teacher from all previous classes
        for class_code in teacher_classes:
            if class_code.startswith(school_code):
                class_ = Class.query.filter_by(class_code=class_code).first()
                class_teachers = eval(class_.teachers)
                class_teachers.remove(teacher_national_code)
                class_.teachers = str(class_teachers)

        # Add the teacher to the new classes
        for class_code in new_classes:
            class_ = Class.query.filter_by(class_code=class_code).first()
            class_teachers = eval(class_.teachers)
            class_teachers.append(teacher_national_code)
            class_.teachers = str(class_teachers)

        # Update the teacher's class list
        teacher_classes.clear()
        teacher_classes.extend(new_classes)
        teacher.teacher_classes = str(teacher_classes)

        db.session.commit()
        return redirect(url_for('teacher_routes.panel_teachers'))

    # Render the form with available classes
    classes = Class.query.filter_by(school_code=current_user.school_code).all()
    return render_template("teacher/edit_teacher.html", classes=classes, teacher=teacher)


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

    if not teacher or teacher.teacher_national_code not in eval(school.teachers):
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
