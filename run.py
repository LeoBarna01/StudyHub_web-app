"""
StudyHub Web Application - Flask Entry Point

This file serves as the Flask application entry point for the StudyHub web application.
It implements the Application Factory pattern and exposes the Flask app instance
for the Flask CLI to use.

Usage:
    flask run                    # Start development server
    flask routes                 # Show all routes  
    flask shell                  # Start Flask shell
    
For production deployment, this file provides the WSGI application object
that can be used with servers like Gunicorn:
    gunicorn run:app

Author: StudyHub Development Team
License: MIT
"""

# Third-party imports
from flask import Flask

# Local application imports  
from app import create_app


# =============================================================================
# FLASK APPLICATION INSTANCE
# =============================================================================

def create_application() -> Flask:
    """
    Create and configure the Flask application instance.
    
    This function uses the Application Factory pattern to create
    a Flask app instance with all necessary configuration.
    
    Returns:
        Flask: Configured Flask application instance ready for use
        
    Note:
        Environment variables are automatically loaded from .flaskenv
        when using the Flask CLI (flask run).
    """
    return create_app()


# Create the Flask application instance
# This variable is used by:
# - Flask CLI commands (flask run, flask routes, etc.)
# - WSGI servers in production (gunicorn run:app)
# - Development tools and testing frameworks
app = create_application()

# =============================================================================
# FLASK CLI INTEGRATION
# =============================================================================

# Additional Flask CLI commands can be registered here if needed
# Example:
# @app.cli.command()
# def init_db():
#     """Initialize the database."""
#     # Database initialization code here
#     pass


# =============================================================================
# PRODUCTION WSGI COMPATIBILITY
# =============================================================================

# The 'app' variable above is automatically used by WSGI servers
# Example production deployment:
# gunicorn --bind 0.0.0.0:8000 run:app

# For development, always use: flask run