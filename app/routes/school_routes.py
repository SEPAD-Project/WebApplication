from flask import render_template, Blueprint
from flask_login import login_required, current_user
from app import db
from app.models.school import School


bp = Blueprint('school_routes', __name__)


@bp.route('/panel/home')
@login_required
def go_to_panel_home():
    return render_template('school/home.html')


@bp.route('/panel/school_info')
@login_required
def go_to_panel_school_info():
    data = School.query.filter(School.school_code == int(current_user.school_code)).first()
    return render_template('school/school_info.html', data=data)