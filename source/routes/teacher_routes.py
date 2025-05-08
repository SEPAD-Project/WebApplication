# Third-party Imports
from flask import Blueprint, redirect, render_template, request, url_for, session
from flask_login import current_user, login_required

# Internal Imports
from source import db
from source.models.models import Class, School, Teacher

# Initialize the Blueprint for teacher-related routes
bp = Blueprint('teacher_routes', __name__)


@bp.route('/panel/teachers')
@login_required
def panel_teachers():
    """
    Display the list of teachers in the current school.

    If a search query is provided (?q=), filter teachers by:
    - Name
    - National code

    Returns:
        Rendered HTML page with teacher list.
    """
    school = School.query.filter(School.id == current_user.id).first()
    teachers = school.teachers

    query = request.args.get('q')
    if query:
        # Filter teachers by name or national code
        teachers = [
            teacher for teacher in teachers
            if (query.lower() in teacher.teacher_name.lower() or
                query.lower() in teacher.teacher_national_code.lower())
        ]

    return render_template('teacher/teachers.html', teachers=teachers)


@bp.route('/panel/teachers/add_teacher', methods=['GET', 'POST'])
@login_required
def add_teacher():
    """
    Handle the process of adding a teacher to the school.

    GET:
        - Render the teacher add form with available classes.

    POST:
        - Validate teacher's credentials.
        - Add them to the school's teacher list and assign selected classes.

    Returns:
        Redirect to teacher list or error page.
    """
    if request.method == 'POST':
        entry_national_code = request.form["teacher_national_code"]
        entry_password = request.form["teacher_password"]

        # Authenticate teacher
        teacher = Teacher.query.filter(
            (Teacher.teacher_national_code == entry_national_code) &
            (Teacher.teacher_password == entry_password)
        ).first()

        if not teacher:
            session["show_error_notif"] = True
            return redirect(url_for("teacher_routes.wrong_teacher_info"))

        # Get selected classes
        selected_classes = request.form.getlist("selected_classes")
        school = School.query.filter(School.id == current_user.id).first()

        # Add teacher to school if not already added
        if teacher not in school.teachers:
            school.teachers.append(teacher)

        # Assign teacher to selected classes
        for class_id in selected_classes:
            class_ = Class.query.filter(Class.id == class_id).first()
            if class_ and teacher not in class_.teachers:
                class_.teachers.append(teacher)

        db.session.commit()
        return redirect(url_for("teacher_routes.panel_teachers"))

    # GET: Render form
    school = School.query.filter(School.id == current_user.id).first()
    return render_template("teacher/add_teacher.html", classes=school.classes)


@bp.route("/panel/teachers/remove_teacher/<teacher_national_code>", methods=['POST', 'GET'])
@login_required
def remove_teacher(teacher_national_code):
    """
    Remove a teacher from the school and their associated classes.

    Returns:
        Redirect to teacher list or error page.
    """
    school = School.query.filter(School.id == current_user.id).first()
    teacher = Teacher.query.filter(
        Teacher.teacher_national_code == teacher_national_code
    ).first()

    if not teacher or teacher not in school.teachers:
        session["show_error_notif"] = True
        return redirect(url_for('teacher_routes.wrong_teacher_info'))

    # Remove teacher from all classes
    for class_ in school.classes:
        if teacher in class_.teachers:
            class_.teachers.remove(teacher)

    # Remove teacher from school
    school.teachers.remove(teacher)

    db.session.commit()
    return redirect(url_for('teacher_routes.panel_teachers'))


@bp.route('/panel/teachers/edit_teacher/<teacher_national_code>', methods=['GET', 'POST'])
@login_required
def edit_teacher(teacher_national_code):
    """
    Edit an existing teacher's class assignments.

    GET:
        - Render the form with current teacher's assigned classes.

    POST:
        - Update teacher's class list based on selected classes.

    Returns:
        Redirect to teacher list or error page.
    """
    school = School.query.filter(School.id == current_user.id).first()
    teacher = Teacher.query.filter(
        Teacher.teacher_national_code == teacher_national_code
    ).first()

    if not teacher or teacher not in school.teachers:
        session["show_error_notif"] = True
        return redirect(url_for('teacher_routes.wrong_teacher_info'))

    if request.method == 'POST':
        # Remove teacher from all current classes
        for class_ in school.classes:
            if teacher in class_.teachers:
                class_.teachers.remove(teacher)

        # Assign teacher to new selected classes
        new_class_codes = request.form.getlist('selected_classes')
        for class_code in new_class_codes:
            class_ = Class.query.filter_by(class_code=class_code).first()
            if class_ and teacher not in class_.teachers:
                class_.teachers.append(teacher)

        db.session.commit()
        return redirect(url_for('teacher_routes.panel_teachers'))

    return render_template("teacher/edit_teacher.html", classes=school.classes, teacher=teacher)


@bp.route("/panel/teachers/teacher_info/<teacher_national_code>")
@login_required
def teacher_info(teacher_national_code):
    """
    Display detailed information about a specific teacher.

    Returns:
        Rendered HTML page with teacher details or error page.
    """
    school = School.query.filter(School.id == current_user.id).first()
    teacher = Teacher.query.filter(
        Teacher.teacher_national_code == teacher_national_code
    ).first()

    if not teacher or teacher not in school.teachers:
        session["show_error_notif"] = True
        return redirect(url_for('teacher_routes.wrong_teacher_info'))

    return render_template('teacher/teacher_info.html', data=teacher)


@bp.route('/panel/teachers/wrong_teacher_info', methods=['GET', 'POST'])
@login_required
def wrong_teacher_info():
    """
    Display an error page for invalid or unrecognized teacher information.

    Returns:
        Redirect to add_teacher form if access is invalid.
        Rendered error page otherwise.
    """
    if not session.pop('show_error_notif', False):
        return redirect(url_for('teacher_routes.add_teacher'))

    return render_template("teacher/wrong_teacher_info.html")
