# Import necessary functions and classes from Flask
from flask import render_template, Blueprint

# Initialize the Blueprint for home-related routes
bp = Blueprint('home_route', __name__)


@bp.route('/')
def home():
    """
    Home page route handler.

    Renders the 'home.html' template.
    Typically used as the landing page for the application.
    """
    return render_template('home.html')


@bp.route('/coming_soon')
def coming_soon():
    """
    "Coming Soon" page route handler.

    Renders a placeholder page (coming_soon.html) indicating that 
    a feature or page is under development.
    """
    return render_template('coming_soon.html')


@bp.route('/contact')
def contact():
    return render_template('contact.html')