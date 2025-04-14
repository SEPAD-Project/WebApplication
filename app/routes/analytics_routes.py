from flask import Blueprint, render_template
from flask_login import login_required

bp = Blueprint('analytics_routes', __name__)

@bp.route('/panel/analytics')
@login_required
def analytics_menu():
    return render_template("analytics/analytics_menu.html")

