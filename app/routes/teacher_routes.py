from flask import render_template, Blueprint
from flask_login import login_required
from app import db


bp = Blueprint('teacher_routes', __name__)


@bp.route('/panel_teachers')
@login_required
def go_to_panel_teachers():
    return render_template('teacher/teachers.html')