from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app.config import Config


db = SQLAlchemy()

login_manager = LoginManager()

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    from app.routes import home_root ,auth_routes, school_routes, class_routes, student_routes, teacher_routes
    app.register_blueprint(home_root.bp)
    app.register_blueprint(auth_routes.bp)
    app.register_blueprint(school_routes.bp)
    app.register_blueprint(class_routes.bp)
    app.register_blueprint(student_routes.bp)
    app.register_blueprint(teacher_routes.bp)

    from app.models.school import School
    @login_manager.user_loader
    def load_user(user_id):
        return School.query.get(int(user_id))

    login_manager.login_view = 'auth_routes.login'

    return app