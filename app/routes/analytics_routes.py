from flask import Blueprint, render_template
from flask_login import login_required
from app.utils.analytics.Generator.analytics_Generator import *
from app.utils.analytics.GUI.analytics_GUI import *


bp = Blueprint('analytics_routes', __name__)

@bp.route('/panel/analytics')
@login_required
def analytics_menu():
    return render_template("analytics/analytics_menu.html")

@bp.route('/panel/analytics/compare_students')
@login_required
def compare_students():
    GUI_compare_students(Generator_compare_students('1051'))
    return render_template("analytics/analytics_menu.html")

@bp.route('/panel/analytics/compare_classes')
@login_required
def compare_classes():
    GUI_compare_classes(Generator_compare_classes())
    return render_template("analytics/analytics_menu.html")

@bp.route('/panel/analytics/compare_teachers')
@login_required
def compare_teachers():
    GUI_compare_teachers(Generator_compare_teachers())
    return render_template("analytics/analytics_menu.html")

@bp.route('/panel/analytics/student_accuracy_week')
@login_required
def student_accuracy_week():
    GUI_student_accuracy_week('Parsa Safaie', Generator_student_over_week('1051', '123'))
    return render_template("analytics/analytics_menu.html")

@bp.route('/panel/analytics/student_accuracy_by_lesson')
@login_required
def student_accuracy_by_lesson():
    GUI_student_accuracy_by_lesson('Parsa Safaie', Generator_student_lessons('1051', '123'))
    return render_template("analytics/analytics_menu.html")