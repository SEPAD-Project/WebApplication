# import modules
from app import db
from app import cache
from app.models._class import Class
from app.models.student import Student
from app.models.teacher import Teacher
from app.utils.generate_class_code import generate_class_code
from app.utils.excel_reading import add_classes
from app.server_side.directory_manager import create_class, edit_class, delete_class

from flask import Blueprint, redirect, render_template, request, url_for, session
from flask_login import current_user, login_required

# Initialize Blueprint
bp = Blueprint('class_routes', __name__)


@bp.route('/panel/classes', methods=['GET', 'POST'])
@cache.cached(timeout=86400)
@login_required
def panel_classes():
    """
    the main section of class part in panel.
    include a list of classes.
    """
    # get the query from form
    query = request.args.get('q')

    if query == "" or query is None:
        # if query is None, all of school classes will be showed
        classes = Class.query.filter(
            Class.school_code == current_user.school_code).all()
    else:
        # if query is not None, school classes will filter by class name and class code
        classes = Class.query.filter(
            (Class.school_code == current_user.school_code) &
            ((Class.class_name.ilike(f'%{query}%')) |
             (Class.class_code.ilike(f'%{query}%')))
        ).all()

    # show the html page for classes list
    return render_template('class/classes.html', classes=classes)


@bp.route('/panel/classes/add_class', methods=['GET', 'POST'])
@cache.cached(timeout=86400)
@login_required
def add_class():
    """
    handle add class section in panel.
    """
    # for POST: get the data from form and start process
    if request.method == 'POST':
        # define and get class registration values
        school_code = current_user.school_code
        class_name = request.form['class_name']
        class_code = generate_class_code(school_code, class_name)
        teachers = "[]"

        # define a new Class with pre-defined values
        new_class = Class(class_name, class_code, school_code, teachers)

        try:
            # add the new class to database
            db.session.add(new_class)
            db.session.commit()
            create_class(school_code=school_code, class_name=class_name)
        except:
            # if the class code is registered before(the school have a class with same name), go to error page
            session["show_error_notif"] = True
            return redirect(url_for('class_routes.duplicated_class_info'))

        # go back to classes list part after successful registration
        return redirect(url_for('class_routes.panel_classes'))

    # for GET: show the html form for add class
    else:
        return render_template('class/add_class.html')


@bp.route('/panel/classes/add_from_excel', methods=['GET', 'POST'])
@cache.cached(timeout=86400)
@login_required
def add_from_excel():
    if request.method == 'POST':
        classes = Class.query.filter(Class.school_code==current_user.school_code).all()
        classes_name = [class_.class_name for class_ in classes]

        file = request.files["file_input"]
        sheet_name = request.form["sheet"]
        name_letter = request.form["name"]

        file.save("classes.xlsx")
        result = add_classes('classes.xlsx', sheet_name, name_letter, classes_name)        

        if result == 'sheet_not_found': 
            text = "Please review your input for sheet name."
            session["show_error_notif"] = True
            return redirect(url_for("class_routes.error_in_excel", text=text))
        
        if result == 'bad_column_letter': 
            text = "Please review your input for column letters."
            session["show_error_notif"] = True
            return redirect(url_for("class_routes.error_in_excel", text=text))
        
        if isinstance(result, tuple):
            if result[0] == "bad_format":
                text = f"Please review the cell { result[2] }{ result[1] } because bad data format."
            elif result[0] == "duplicated_name":
                text = f"Please review the cell { result[2] }{ result[1] } because duplicated value."
            else:
                text = f"Please review the cell { result[2] }{ result[1] } because unknown trouble."

            session["show_error_notif"] = True
            return redirect(url_for("class_routes.error_in_excel", text=text))
        

        for class_ in result:
            new_class = Class(class_name=class_['name'], class_code=class_['code'], school_code=current_user.school_code, teachers='[]')
            db.session.add(new_class)
        db.session.commit()

        return redirect(url_for('class_routes.panel_classes'))

    else:
        return render_template("class/add_from_excel.html")
    

@bp.route('/panel/classes/edit_class/<class_name>', methods=['GET', 'POST'])
@cache.cached(timeout=86400)
@login_required
def edit_class(class_name):
    """
    handle edit class section in panel.
    """
    # for POST: get the data from form and start process
    if request.method == "POST":
        # define and get desired class values
        new_name = request.form['class_name']
        new_code = generate_class_code(current_user.school_code, new_name)
        old_code = generate_class_code(current_user.school_code, class_name)

        # search database with values and define the class object
        class_ = Class.query.filter(Class.class_code == old_code).first()

        # if class don't exists(the class name is manipulated by the user), then go to error page
        if class_ == None:
            return redirect(url_for('class_routes.unknown_class_info'))

        # redefine class values in database
        class_.class_code = new_code
        class_.class_name = new_name

        # redefine class code for each student of class
        students = Student.query.filter(Student.class_code == old_code).all()
        for student in students:
            student.class_code = new_code

        # redefine classes list for each teacher of class
        teachers_national_code = eval(class_.teachers)
        for teacher_national_code in teachers_national_code:
            teacher = Teacher.query.filter(
                Teacher.teacher_national_code == teacher_national_code).first()
            teacher_classes = eval(teacher.teacher_classes)
            index = teacher_classes.index(old_code)
            teacher_classes[index] = new_code
            teacher.teacher_classes = str(teacher_classes)

        try:
            # commit changes in database
            db.session.commit()
            edit_class(school_code=current_user.school_code, old_class_name=class_name, new_class_name=new_name)
        except:
            # if the new class name was registered before(by user-self), go to error page
            session["show_error_notif"] = True
            return redirect(url_for('class_routes.duplicated_class_info'))

        # go back to classes list part after successful registration
        return redirect(url_for('class_routes.panel_classes'))

    # for GET: show the html form for edit class with class values
    else:
        # define class code
        school_code = current_user.school_code
        class_code = generate_class_code(school_code, class_name)

        # search for class object with same values
        class_ = Class.query.filter(Class.class_code == class_code).first()

        # if class don't exists, go to error page
        if class_ == None:
            session["show_error_notif"] = True
            return redirect(url_for('class_routes.unknown_class_info'))

        # show edit class page with class name
        return render_template('class/edit_class.html', name=class_.class_name)


@bp.route('/panel/classes/remove/<class_name>', methods=['GET', 'POST'])
@cache.cached(timeout=86400)
@login_required
def remove_class(class_name):
    """
    handle remove class section in panel.
    """
    # generate class code for extract class object from database
    class_code = generate_class_code(current_user.school_code, class_name)

    # define class object and delete its row from database
    class_ = Class.query.filter(Class.class_code == class_code).first()
    db.session.delete(class_)

    # delete students of desired class
    students = Student.query.filter(Student.class_code == class_code).all()
    for student in students:
        db.session.delete(student)

    # delete class code from the classes list of teachers of desired class
    teachers_national_code = eval(class_.teachers)
    for national_code in teachers_national_code:
        teacher = Teacher.query.filter(
            Teacher.teacher_national_code == national_code).first()
        teacher_classes = eval(teacher.teacher_classes)
        teacher_classes.remove(class_code)
        teacher.teacher_classes = str(teacher_classes)

    # commit all changes and go back to classes list(main section of classes part)
    db.session.commit()
    delete_class(school_code=current_user.school_code, class_name=class_name)
    return redirect(url_for('class_routes.panel_classes'))


@bp.route('/panel/classes/class_info/<class_name>')
@cache.cached(timeout=86400)
@login_required
def class_info(class_name):
    """
    handle class info section in panel.
    """
    # generate class code for class object extracting
    school_code = current_user.school_code
    class_code = generate_class_code(school_code, class_name)

    # extract class object and check its availability
    class_ = Class.query.filter(Class.class_code == class_code).first()
    if class_ == None:
        # return error page if there is not class with that information
        session["show_error_notif"] = True
        return redirect(url_for('class_routes.unknown_class_info'))

    # extract all teachers and students of class from database for show them in info page
    teachers = [Teacher.query.filter(Teacher.teacher_national_code == national_code).first(
    ) for national_code in eval(class_.teachers)]
    students = Student.query.filter(
        Student.class_code == class_.class_code).all()

    # show info page with values
    return render_template('class/class_info.html', data=class_, teachers=teachers, students=students)


@bp.route('/unknown_class_info')
@cache.cached(timeout=86400)
def unknown_class_info():
    if not session.get('show_error_notif', False):
        return redirect(url_for('class_routes.panel_classes'))
    session.pop('show_error_notif', None)
    return render_template('class/unknown_class_info.html')


@bp.route('/panel/classes/duplicated_class_info')
@cache.cached(timeout=86400)
@login_required
def duplicated_class_info():
    if not session.get('show_error_notif', False):
        return redirect(url_for('class_routes.add_class'))
    session.pop('show_error_notif', None)
    return render_template('class/duplicated_class_info.html')


@bp.route("/panel/classes/error_in_excel/<text>", methods=['GET', 'POST'])
@cache.cached(timeout=86400)
@login_required
def error_in_excel(text):
    if not session.get('show_error_notif', False):
        return redirect(url_for('class_routes.add_from_excel'))
    session.pop('show_error_notif', None)
    return render_template('class/error_in_excel.html', text=text)