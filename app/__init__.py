# Standard Library Imports

# Third-party Imports
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_compress import Compress

# Internal Imports
from app.config import Config

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    """
    Create and configure the Flask application.

    Sets up extensions (DB, login manager, compression, rate limiting), config,
    routes (via blueprints), and error handling.

    Returns:
        Flask: The configured Flask application instance.
    """
    # Create Flask app instance
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(Config)

    # Initialize core extensions
    db.init_app(app)
    login_manager.init_app(app)
    Compress(app)

    # Register blueprints
    from app.routes import (
        home_routes, auth_routes, school_routes,
        class_routes, student_routes, teacher_routes, analytics_routes
    )
    app.register_blueprint(home_routes.bp)
    app.register_blueprint(auth_routes.bp)
    app.register_blueprint(school_routes.bp)
    app.register_blueprint(class_routes.bp)
    app.register_blueprint(student_routes.bp)
    app.register_blueprint(teacher_routes.bp)
    app.register_blueprint(analytics_routes.bp)

    # Custom 404 page handler
    @app.route('/<path:unknown_path>')
    def unknown_path(unknown_path):
        return render_template('404.html')

    # Flask-Login user loader
    from app.models.models import School

    @login_manager.user_loader
    def load_user(user_id):
        return School.query.get(int(user_id))

    # Set the login view for unauthorized redirects
    login_manager.login_view = 'auth_routes.login'

    # Set up rate limiting
    Limiter(app=app, key_func=get_remote_address, default_limits=["10/minute"])

    # Ensure database tables exist
    with app.app_context():
        db.create_all()

    return app
