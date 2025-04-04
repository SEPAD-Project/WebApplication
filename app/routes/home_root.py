# Import necessary functions and classes from Flask
from flask import render_template, Blueprint

# Initialize the Blueprint for home-related routes
# This allows you to group views logically and register them later in the app
bp = Blueprint('home_route', __name__)


@bp.route('/')
def home():
    """
    Home page route handler.
    
    This function is triggered when the root URL '/' is accessed.
    - It simply renders the 'home.html' template.
    - Typically used as the landing page for the application.
    """
    return render_template('home.html')


@bp.route('/coming_soon')
def coming_soon():
    """
    "Coming Soon" page route handler.
    
    This function handles the '/coming_soon' URL.
    - Renders a placeholder page (coming_soon.html) indicating that a feature or page is under development.
    - Useful for directing users to a clean page while new features are being built.
    """
    return render_template('coming_soon.html')
