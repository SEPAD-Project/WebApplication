from flask import render_template, Blueprint

# Initialize the Blueprint for home-related routes
bp = Blueprint('home_route', __name__)


@bp.route('/')
def go_to_home():
    """
    Handles the home page of the application.
    - Renders the 'home.html' template.
    """
    return render_template('home.html')