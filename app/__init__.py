from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from app.config import Config
from flask_compress import Compress

# Initialize the SQLAlchemy database instance
db = SQLAlchemy()

# Initialize the LoginManager instance
login_manager = LoginManager()

def create_app():
    """
    Creates and configures the Flask application with necessary extensions.
    
    This function sets up the application with configurations, database,
    user login management, request rate limiting, compression, and blueprint registration.
    
    Returns:
        Flask app instance: The configured Flask application.
    """

    # Initialize the Flask app, specifying the template and static folders
    app = Flask(__name__, template_folder='templates', static_folder='static')
    # Load configuration from the Config class
    app.config.from_object(Config)

    # Initialize the extensions with the app
    db.init_app(app)
    login_manager.init_app(app)

    # Apply Flask-Compress to the app for compression of responses
    Compress(app)

    # Register all the blueprints for different parts of the application
    from app.routes import home_root, auth_routes, school_routes, class_routes, student_routes, teacher_routes, analytics_routes
    app.register_blueprint(home_root.bp)
    app.register_blueprint(auth_routes.bp)
    app.register_blueprint(school_routes.bp)
    app.register_blueprint(class_routes.bp)
    app.register_blueprint(student_routes.bp)
    app.register_blueprint(teacher_routes.bp)
    app.register_blueprint(analytics_routes.bp)

    # Catch-all route for unknown paths (404 error page)
    @app.route('/<path:unknown_path>')
    def unknown_path(unknown_path):
        # Render a 404 page if an unknown path is requested
        return render_template('404.html')

    # Define the user loader for Flask-Login (loads user from database)
    from app.models.models import School
    @login_manager.user_loader
    def load_user(user_id):
        # Query the database to load the user by their ID
        return School.query.get(int(user_id))

    # Define the view to redirect to when login is required
    login_manager.login_view = 'auth_routes.login'

    # Initialize rate limiter with a default limit (10 requests per minute)
    limiter = Limiter(app=app, key_func=get_remote_address, default_limits=["10/minute"])

    # Create the database tables if they don't already exist
    with app.app_context():
        db.create_all()

    return app
