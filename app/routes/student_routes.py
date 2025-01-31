from flask import render_template, Blueprint
from flask_login import login_required
from app import db


bp = Blueprint('student_routes', __name__)


@bp.route('/panel_students')
@login_required
def go_to_panel_students():
    return render_template('student/students.html')