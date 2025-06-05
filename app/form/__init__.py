"""
StudyHub Contact Forms Blueprint

This module handles contact forms and support requests within the StudyHub application.
It provides functionality for users to submit questions, feedback, and support requests
through web forms.

Blueprint Structure:
    - forms.py: WTForms form definitions and validation
    - form.py: Route handlers for form processing and rendering

Key Features:
    - Contact form for general inquiries
    - Question submission system
    - Email integration for notifications
    - Database storage of all submissions
    - CSRF protection and input validation

URL Prefix: /form
Main Routes:
    - /form/form: Contact form page
    
Security Features:
    - WTForms CSRF protection
    - Input sanitization and validation
    - Email format validation
    - Content length limits

Author: StudyHub Development Team
License: MIT
"""

from flask import Blueprint

# Create the forms blueprint with URL prefix /form
bp = Blueprint('form', __name__)

# Import route handlers and form definitions
# This import is placed after blueprint creation to avoid circular imports
from app.form import form, forms
