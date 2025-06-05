"""
app/main/errors.py - Global Error Handlers

This module defines application-wide error handlers for common HTTP errors.
Error handlers provide user-friendly error pages instead of default browser errors.

Supported Error Codes:
- 404 Not Found: When a requested page/resource doesn't exist
- 500 Internal Server Error: When server encounters an unexpected error

The @bp.app_errorhandler decorator makes these handlers global across the entire app.
"""

from flask import render_template
from . import bp

# ============================================================================
# GLOBAL ERROR HANDLERS
# ============================================================================

@bp.app_errorhandler(404)
def not_found_error(error):
    """
    Handle 404 Not Found errors.
    
    This handler is triggered when:
    - User navigates to a non-existent route
    - A resource (file, image, etc.) is not found
    - Invalid URLs are accessed
    
    Args:
        error: The error object containing details about the 404 error
        
    Returns:
        Tuple: (rendered 404 template, 404 status code)
    """
    return render_template('errors/404.html'), 404


@bp.app_errorhandler(500)
def internal_error(error):
    """
    Handle 500 Internal Server Error.
    
    This handler is triggered when:
    - Unhandled exceptions occur in the application
    - Database connection errors
    - Server configuration issues
    - Any unexpected server-side errors
    
    Args:
        error: The error object containing details about the 500 error
        
    Returns:
        Tuple: (rendered 500 template, 500 status code)
    """
    return render_template('errors/500.html'), 500
