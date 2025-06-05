"""
app/main/__init__.py - Main Blueprint Initialization

This file creates the 'main' blueprint for the primary application routes.
The main blueprint handles:
- Homepage/landing page for non-authenticated users
- Dashboard for authenticated users
- Error handling (404, 500)

Blueprint pattern allows modular organization of routes in Flask applications.
"""

from flask import Blueprint

# Create the main blueprint
# This blueprint handles core application pages (home, dashboard)
bp = Blueprint('main', __name__)

# Import route handlers and error handlers
# This must be done after blueprint creation to avoid circular imports
from app.main import main, errors