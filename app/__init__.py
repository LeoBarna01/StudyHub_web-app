from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
db = SQLAlchemy()
login = LoginManager()
# Redirect unauthorized users to the login page
login.login_view = 'auth.login'
login.login_message_category = 'warning'


def create_app(config_object='config.Config'):
    """
    Application factory for StudyHub.
    - Creates and configures the Flask app
    - Initializes extensions (SQLAlchemy, LoginManager)
    - Registers blueprints: main, auth, upload, view, form
    - Sets up context processors and error handlers
    """
    app = Flask(__name__, template_folder="../templates")
    # Load configuration (SECRET_KEY, DATABASE_URI, UPLOAD_FOLDER, etc.)
    app.config.from_object(config_object)

    # Initialize extensions with app
    db.init_app(app)
    login.init_app(app)

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

    # Context processor: inject current UTC year into all templates (actually we used it for the footer mainly just to add something realistic)
    @app.context_processor
    def inject_current_year():
        from datetime import datetime
        return {'current_year': datetime.utcnow().year}


    return app