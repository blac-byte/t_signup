from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .utils.errors import register_error_handlers

db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_class="app.config.Config"):
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Security configs
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "signin" #------------- redirects here if not logged in

    @login_manager.user_loader
    def load_user(user_id):
        return student.query.get(int(user_id))

    # Import models so db.create_all() knows them
    from app.models import student, time, course, classes
    with app.app_context():
        db.create_all()
        course.insert_sample_courses() 

    # Register blueprints (routes)
    from app.routes.auth import bp as main_routes
    app.register_blueprint(main_routes)

    # Register blueprints (services)
    from app.services.parser import bp as parser
    app.register_blueprint(parser)

    # Register blueprints (services)
    from app.services.schedule import bp as schedule
    app.register_blueprint(schedule)

    # Error handlers
    from app.utils.errors import register_error_handlers
    register_error_handlers(app)

    return app
