"""
StudyHub Application Configuration

This module contains all configuration settings for the StudyHub Flask application.
It implements the Config Class pattern to organize application settings in a
centralized and maintainable way.

Configuration Categories:
    - Security: Secret keys, CSRF protection, session management
    - Database: SQLAlchemy settings, connection strings
    - File Upload: Upload directories, file size limits, allowed extensions
    - Email: SMTP settings for contact forms and notifications
    - Environment: Development vs Production configurations

The configuration system supports:
    - Environment variable overrides for production deployment
    - Secure defaults for development
    - Easy switching between different environments
    - Separation of sensitive data from code

Usage:
    app.config.from_object('config.Config')

Security Notes:
    - Never commit sensitive data like SECRET_KEY to version control
    - Use environment variables for production secrets
    - Regularly rotate secret keys and database passwords
    - Ensure upload directories have proper permissions

Author: StudyHub Development Team
License: MIT
"""

import os  # Operating system interface for file paths and environment variables

# =============================================================================
# PROJECT DIRECTORY SETUP
# =============================================================================

# Determine the base directory of the project (where this config file is located)
# This provides a reliable reference point for all relative paths in the application
basedir = os.path.abspath(os.path.dirname(__file__))

# =============================================================================
# MAIN APPLICATION CONFIGURATION CLASS
# =============================================================================

class Config:
    """
    Main configuration class for the StudyHub application.
    
    This class centralizes all application settings, making them easily
    accessible throughout the application and simplifying configuration
    management across different deployment environments.
    
    Configuration Philosophy:
        - Environment variables override defaults for production security
        - Sensible defaults for development and testing
        - Clear separation between different types of configuration
        - Comprehensive documentation for each setting
    
    Attributes:
        SECRET_KEY: Cryptographic key for session security and CSRF protection
        SQLALCHEMY_DATABASE_URI: Database connection string
        SQLALCHEMY_TRACK_MODIFICATIONS: SQLAlchemy event tracking (disabled for performance)
        UPLOAD_FOLDER: Directory path for user-uploaded files
        MAX_CONTENT_LENGTH: Maximum file upload size in bytes
        MAIL_*: SMTP configuration for email functionality
    """
    
    # =============================================================================
    # SECURITY CONFIGURATION
    # =============================================================================
    
    # Secret key for signing session cookies and CSRF tokens
    # CRITICAL: In production, this MUST be set as an environment variable
    # and should be a long, random string that is kept secret
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-change-in-production'

    # =============================================================================
    # DATABASE CONFIGURATION
    # =============================================================================
    
    # Database connection URI
    # Development: Uses SQLite for simplicity and portability
    # Production: Override with DATABASE_URL environment variable (PostgreSQL/MySQL)
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('DATABASE_URL') or
        'sqlite:///' + os.path.join(basedir, 'app.db')  # SQLite file in project root
    )
    
    # Disable SQLAlchemy event tracking to improve performance
    # This feature is rarely needed and consumes memory
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # =============================================================================
    # FILE UPLOAD CONFIGURATION
    # =============================================================================
    
    # Directory where user-uploaded files are stored
    # Must be writable by the web server process
    UPLOAD_FOLDER = os.path.join(basedir, 'uploads')
    
    # Maximum file upload size: 16 MB
    # This prevents abuse and ensures reasonable server resource usage
    # Users trying to upload larger files will receive a clear error message
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB in bytes    # =============================================================================
    # EMAIL CONFIGURATION (OPTIONAL)
    # =============================================================================
    
    # SMTP server configuration for sending emails
    # Used for contact forms, password resets, and system notifications
    # All email settings should be configured via environment variables
    
    # SMTP server hostname (e.g., smtp.gmail.com, smtp.outlook.com)
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    
    # SMTP server port (587 for TLS, 465 for SSL, 25 for unencrypted)
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    
    # Enable TLS encryption for secure email transmission
    # Recommended for production environments
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    
    # SMTP authentication credentials
    # Should be set as environment variables for security
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')  # SMTP username/email
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')  # SMTP password/app password
    
    # =============================================================================
    # ADDITIONAL CONFIGURATION NOTES
    # =============================================================================
    """
    Environment Variable Setup for Production:
    
    Required:
        export SECRET_KEY="your-very-long-random-secret-key"
        export DATABASE_URL="postgresql://user:pass@localhost/studyhub"
    
    Optional (for email functionality):
        export MAIL_SERVER="smtp.gmail.com"
        export MAIL_PORT="587"
        export MAIL_USE_TLS="1"
        export MAIL_USERNAME="your-email@gmail.com"
        export MAIL_PASSWORD="your-app-password"
    
    File Permissions:
        - Ensure the uploads/ directory is writable by the web server
        - Set appropriate permissions: chmod 755 uploads/
        - Consider using a separate file server for production
    
    Security Considerations:
        - Regularly rotate SECRET_KEY in production
        - Use strong, unique passwords for database and email
        - Implement rate limiting for file uploads
        - Validate all uploaded files before processing
        - Consider using cloud storage for uploaded files in production
    """