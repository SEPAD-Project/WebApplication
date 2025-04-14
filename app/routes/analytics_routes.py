from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from app.utils.analytics.Generator.analytics_Generator import *
from app.utils.analytics.GUI.analytics_GUI import *
from app.utils.generate_class_code import reverse_class_code
from app.models.school import School
from app.server_side.Website.send_email import send_styled_email
from threading import Thread


bp = Blueprint('analytics_routes', __name__)

@bp.route('/panel/analytics')
@login_required
def analytics_menu():
    return render_template("analytics/analytics_menu.html")

@bp.route('/panel/analytics/compare_students', methods=['GET', 'POST'])
@login_required
def compare_students():
    if request.method == "POST":
        class_code = request.form['selected_class']
        class_name = reverse_class_code(class_code)[1]
        GUI_compare_students(Generator_compare_students(class_name))
        Thread(target=send_styled_email(School.query.filter(School.school_code==current_user.school_code).first().email, 'Compare Students', "c:\sap-project\server\compare_students.pdf")).start()
        return render_template("analytics/analytics_menu.html")
    
    classes = Class.query.filter(Class.school_code==current_user.school_code).all()
    return render_template('analytics/class_name_for_compare_students.html', classes=classes)

@bp.route('/panel/analytics/compare_classes')
@login_required
def compare_classes():
    GUI_compare_classes(Generator_compare_classes())
    Thread(target=send_styled_email(School.query.filter(School.school_code==current_user.school_code).first().email, 'Compare Classes', "c:\sap-project\server\compare_classes.pdf")).start()
    return render_template("analytics/analytics_menu.html")

@bp.route('/panel/analytics/compare_teachers')
@login_required
def compare_teachers():
    GUI_compare_teachers(Generator_compare_teachers())
    Thread(target=send_styled_email(School.query.filter(School.school_code==current_user.school_code).first().email, 'Compare Teachers', "c:\sap-project\server\compare_teachers.pdf")).start()
    return render_template("analytics/analytics_menu.html")

@bp.route('/panel/analytics/student_accuracy_week', methods=['GET', 'POST'])
@login_required
def student_accuracy_week():
    if request.method == "POST":
        student_nc = request.form['student_national_code']
        student = Student.query.filter(Student.student_national_code==student_nc).first()
        GUI_student_accuracy_week(student.student_name+' '+student.student_family, Generator_student_over_week(reverse_class_code(student.class_code)[1], student_nc))
        Thread(target=send_styled_email(School.query.filter(School.school_code==current_user.school_code).first().email, 'Student Accuracy Over the Week', "c:\sap-project\server\student_accuracy_week.pdf")).start()
        return render_template("analytics/analytics_menu.html")
    
    return render_template("analytics/student_nc_for_accuracy_week.html")

@bp.route('/panel/analytics/student_accuracy_by_lesson', methods=['GET', 'POST'])
@login_required
def student_accuracy_by_lesson():
    if request.method == "POST":
        student_nc = request.form['student_national_code']
        student = Student.query.filter(Student.student_national_code==student_nc).first()
        GUI_student_accuracy_by_lesson(student.student_name+' '+student.student_family, Generator_student_lessons(reverse_class_code(student.class_code)[1], student_nc))
        Thread(target=send_styled_email(School.query.filter(School.school_code==current_user.school_code).first().email, 'Student Accuracy By lesson', "c:\sap-project\server\student_accuracy_by_lesson.pdf")).start()
        return render_template("analytics/analytics_menu.html")
    
    return render_template("analytics/student_nc_for_accuracy_lesson.html")
