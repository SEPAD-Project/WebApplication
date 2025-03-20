from flask import render_template, Blueprint
from app import cache

# Initialize the Blueprint for home-related routes
bp = Blueprint('home_route', __name__)


@bp.route('/')
@cache.cached(timeout=86400)
def home():
    """
    Handles the home page of the application.
    - Renders the 'home.html' template.
    """
    return render_template('home.html')

@bp.route('/coming_soon')
@cache.cached(timeout=86400)
def coming_soon():
    """
    Handles the coming soon page of the application.
    - Renders the 'coming_soon.html' template.
    """
    return render_template('coming_soon.html')