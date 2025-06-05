"""
app/view/__init__.py - Document Viewing Blueprint Initialization

This file creates the 'view' blueprint for document browsing and management.
The view blueprint handles:
- Document search and filtering functionality
- Document downloads and previews
- Favorites management (add/remove favorites)
- User's uploaded documents display
- Document deletion by owners

Blueprint pattern allows modular organization of viewing-related routes.
"""

from flask import Blueprint

# Create the view blueprint
# This blueprint handles all document viewing and management functionality
bp = Blueprint('view', __name__)

# Import route handlers and utilities after blueprint creation
# This prevents circular import issues
from app.view import view, utils
