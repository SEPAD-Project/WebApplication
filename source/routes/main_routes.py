# Third-party Imports
from flask import render_template, Blueprint, send_from_directory

# Initialize the Blueprint for home-related routes
bp = Blueprint('main_routes', __name__)


@bp.route('/')
def home():
    """
    Render the home (landing) page.

    Returns:
        Rendered HTML for 'home.html'.
    """
    return render_template('home.html')


@bp.route('/coming_soon')
def coming_soon():
    """
    Render the 'Coming Soon' placeholder page.

    Returns:
        Rendered HTML for 'coming_soon.html'.
    """
    return render_template('coming_soon.html')


@bp.route('/contact')
def contact():
    """
    Render the contact page.

    Returns:
        Rendered HTML for 'contact.html'.
    """
    return render_template('contact.html')


@bp.route('/downloads')
def downloads():
    """
    Render the downloads page.

    Returns:
        Rendered HTML for 'downloads.html'.
    """
    return render_template('downloads.html')


@bp.route('/about')
def about():
    """
    Render the about page.

    Returns:
        Rendered HTML for 'about.html'.
    """
    return render_template('about.html')


@bp.route('/download_documentation/<document>')
def download_documentation(document):
    return send_from_directory(
        r'C:\Users\Administrator\Documents\mostanadat',
        document,
        as_attachment=False
    )
