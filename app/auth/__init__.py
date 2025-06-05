"""
app/auth/__init__.py - Authentication Blueprint Initialization

This file creates the 'auth' blueprint for user authentication functionality.
The auth blueprint handles:
- User registration and login/logout
- Profile management and image uploads
- Password management and validation
- User session management

Blueprint pattern allows modular organization of authentication routes.
"""

from flask import Blueprint

# Create the authentication blueprint
# This blueprint handles all user authentication and profile management
bp = Blueprint('auth', __name__)

# Import route handlers after blueprint creation to avoid circular imports
# This pattern is essential in Flask to prevent import cycles
from app.auth import routes
