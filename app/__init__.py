"""
StudyHub Application Factory

This module implements the Flask Application Factory pattern for the StudyHub
web application. It handles application creation, configuration, extension 
initialization, and blueprint registration.

The Application Factory pattern enables:
- Multiple application instances with different configurations
- Clean separation between configuration and application logic
- Easy testing with different configurations
- Flexible deployment scenarios (development, testing, production)

Application Architecture:
    - main: Core pages (home, dashboard, error handling)
    - auth: User authentication (login, register, profile management)
    - upload: Document upload and file management
    - view: Document viewing, searching, and favorites
    - form: Contact forms and support requests

Key Features:
    - SQLAlchemy ORM for database operations
    - Flask-Login for user session management
    - Flask-Migrate for database schema migrations
    - Modular blueprint architecture
    - Custom template filters and context processors
    - Security-focused configuration

Author: StudyHub Development Team
License: MIT
"""

# =============================================================================
# CORE IMPORTS AND DEPENDENCIES
# =============================================================================

# Flask core framework
from flask import Flask

# Database and ORM
from flask_sqlalchemy import SQLAlchemy

# User authentication and session management  
from flask_login import LoginManager

# Database migration system
from flask_migrate import Migrate

# =============================================================================
# GLOBAL EXTENSION INSTANCES
# =============================================================================

# Initialize extension instances that will be configured with the app
# These are created here but initialized in the application factory
db = SQLAlchemy()          # Database ORM for model operations
login = LoginManager()     # User session and authentication management
migrate = Migrate()        # Database schema migration system

# =============================================================================
# FLASK-LOGIN CONFIGURATION
# =============================================================================

def configure_login_manager():
    """
    Configure Flask-Login settings for user authentication.
    
    This function sets up the login manager with appropriate
    settings for user experience and security.
    """
    # Redirect unauthorized users to login page
    login.login_view = 'auth.login'
    
    # Flash message category for Bootstrap styling
    login.login_message_category = 'warning'
    
    # Custom message for login required
    login.login_message = 'Please log in to access this page.'
    
    # Session protection level
    login.session_protection = 'strong'  # Protects against session hijacking

# ============================================================================
# APPLICATION FACTORY
# ============================================================================

def create_app(config_object='config.Config'):
    """
    StudyHub Application Factory.
    
    This pattern enables creating multiple application instances
    with different configurations (development, testing, production).
    
    Operations performed:
    1. Create Flask instance with custom paths
    2. Load application configuration
    3. Initialize Flask extensions
    4. Import database models
    5. Register blueprints (application modules)
    6. Configure template context processors and filters
    
    Args:
        config_object (str): Configuration class to use for the application.
                           Defaults to 'config.Config' for production settings.
        
    Returns:
        Flask: Configured Flask application instance ready for deployment.
        
    Example:
        # Create application with default configuration
        app = create_app()
        
        # Create application with custom configuration
        app = create_app('config.TestingConfig')
    """
    
    # Create Flask instance with custom directory structure
    app = Flask(__name__, 
                template_folder="../templates",  # HTML templates in project root
                static_folder="../static",       # Static files (CSS, JS, images)
                static_url_path="/static")       # URL path for serving static files
    
    # Load configuration from specified config object
    # Contains SECRET_KEY, DATABASE_URI, and other app settings
    app.config.from_object(config_object)

    # =============================================================================
    # EXTENSION INITIALIZATION
    # =============================================================================
    
    # Connect extensions to the Flask application instance
    db.init_app(app)              # SQLAlchemy for database operations
    migrate.init_app(app, db)     # Flask-Migrate for database schema migrations
    
    # Configure Flask-Login settings
    login.init_app(app)           # User authentication and session management
    configure_login_manager()     # Apply custom login manager configuration

    # Import database models after database initialization
    # This ensures SQLAlchemy is ready to define database tables
    from app import models

    # =============================================================================
    # BLUEPRINT REGISTRATION (APPLICATION MODULES)
    # =============================================================================
    
    # Main pages blueprint (home, dashboard, error handling)
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    # Authentication blueprint (login, registration, profile management)
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # Document upload blueprint (file upload and management)
    from app.upload import bp as upload_bp
    app.register_blueprint(upload_bp, url_prefix='/upload')

    # Document viewing blueprint (search, preview, favorites)
    from app.view import bp as view_bp
    app.register_blueprint(view_bp, url_prefix='/view')

    # Contact forms blueprint (support and feedback)
    from app.form import bp as form_bp
    app.register_blueprint(form_bp, url_prefix='/form')

    # =============================================================================
    # TEMPLATE CONTEXT PROCESSORS AND CUSTOM FILTERS
    # =============================================================================

    @app.context_processor
    def inject_current_year():
        """
        Template context processor that injects the current year into all templates.
        
        This is primarily used in the footer to display "© 2024 StudyHub".
        The function is automatically executed for every request, making the
        current year available as a template variable.
        
        Returns:
            dict: Dictionary containing 'current_year' key with current year value.
            
        Usage in templates:
            <footer>© {{ current_year }} StudyHub. All rights reserved.</footer>
        """
        from datetime import datetime
        return {'current_year': datetime.utcnow().year}

    @app.template_filter('nl2br')
    def nl2br_filter(text):
        """
        Custom template filter that converts newlines (\\n) to HTML <br> tags.
        
        This filter is useful for displaying text with line breaks in HTML templates,
        particularly for user-generated content like document descriptions or comments.
        
        Args:
            text (str): Input text that may contain newline characters.
            
        Returns:
            str: Text with newlines replaced by <br> tags, or original text if None.
            
        Usage in templates:
            {{ document.description|nl2br|safe }}
            
        Note:
            Remember to use the 'safe' filter to prevent HTML escaping of <br> tags.
        """
        if text:
            return text.replace('\n', '<br>')
        return text

    return app