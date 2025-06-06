# STUDYHUB WEB APPLICATION - FLASK ENVIRONMENT CONFIGURATION
# ================================================================
#
# PURPOSE:
# - Defines Flask application environment variables for development
# - Configures Flask development server settings
# - Sets up debugging and development features
# - Automatically loaded by python-dotenv in Flask applications
#
# CONFIGURATION:
# - Development environment with debug mode enabled
# - Local server configuration for development
# - Automatic reloading for code changes
# - Standard Flask development port and host
#
# USAGE:
# - This file is automatically read by Flask when using 'flask run'
# - Variables are loaded as environment variables at startup
# - Used for local development environment only
#
# SECURITY NOTE:
# - Debug mode should NEVER be enabled in production
# - This configuration is for development environment only
#
# AUTHOR: StudyHub Development Team
# LAST MODIFIED: 2024

FLASK_APP=run.py                    # Entry point file for Flask application
FLASK_ENV=development               # Set Flask environment to development mode
FLASK_DEBUG=1                       # Enable debug mode for detailed error messages and auto-reload
FLASK_RUN_PORT=5000                 # Set development server port to 5000 (Flask default)
FLASK_RUN_HOST=127.0.0.1           # Bind server to localhost (local development only)
WERKZEUG_RELOADER_TYPE=stat        # Use stat-based file monitoring for auto-reload (better for some systems) 
