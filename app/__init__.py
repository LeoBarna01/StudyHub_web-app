from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
login = LoginManager()
migrate = Migrate()

# Redirect unauthorized users to the login page
login.login_view = 'auth.login'
login.login_message_category = 'warning'


def create_app(config_object='config.Config'):
    """
    Application factory for StudyHub.
    - Creates and configures the Flask app
    - Initializes extensions (SQLAlchemy, LoginManager)
    - Registers blueprints: main, auth, upload, view, form, forum
    - Sets up context processors and error handlers
    """
    app = Flask(__name__, 
                template_folder="../templates",
                static_folder="../static",
                static_url_path="/static")
    # Load configuration (SECRET_KEY, DATABASE_URI, UPLOAD_FOLDER, etc.)
    app.config.from_object(config_object)

    # Initialize extensions with app
    db.init_app(app)
    login.init_app(app)
    migrate.init_app(app, db)

    # Import models here to ensure db is initialized
    from app import models

    # Register blueprints
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.upload import bp as upload_bp
    app.register_blueprint(upload_bp, url_prefix='/upload')

    from app.view import bp as view_bp
    app.register_blueprint(view_bp, url_prefix='/view')

    from app.form import bp as form_bp
    app.register_blueprint(form_bp, url_prefix='/form')

    from app.forum import bp as forum_bp
    app.register_blueprint(forum_bp, url_prefix='/forum')

    # Context processor: inject current UTC year into all templates (actually we used it for the footer mainly just to add something realistic)
    @app.context_processor
    def inject_current_year():
        from datetime import datetime
        return {'current_year': datetime.utcnow().year}

    # Custom filter to replace newlines with <br> tags
    @app.template_filter('nl2br')
    def nl2br_filter(s):
        if s:
            return s.replace('\n', '<br>')
        return s


    return app