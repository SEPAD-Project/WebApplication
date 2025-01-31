from flask import render_template, Blueprint


bp = Blueprint('home_route', __name__)


@bp.route('/')
def go_to_home():
    return render_template('home.html')