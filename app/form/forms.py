"""
StudyHub Contact Forms

This module defines WTForms classes for handling user contact and support requests.
All forms include comprehensive validation, CSRF protection, and user-friendly
error messages.

Forms Available:
    - QuestionForm: General contact/question submission form

Security Features:
    - CSRF token validation (FlaskForm inheritance)
    - Input length validation to prevent abuse
    - Email format validation
    - Required field validation
    - XSS protection through proper input handling

Author: StudyHub Development Team
License: MIT
"""

# =============================================================================
# CORE IMPORTS
# =============================================================================

# Flask-WTF for form handling and CSRF protection
from flask_wtf import FlaskForm

# WTForms field types for different input types
from wtforms import SelectField, StringField, TextAreaField, SubmitField

# WTForms validators for input validation and security
from wtforms.validators import DataRequired, Email, Length

# =============================================================================
# CONTACT FORM DEFINITIONS
# =============================================================================

class QuestionForm(FlaskForm):
    """
    Contact form for user questions and support requests.
    
    This form allows users to submit questions, feedback, or support requests
    to the StudyHub team. All submissions are validated, stored in the database,
    and optionally forwarded via email.
    
    Fields:
        subject (StringField): The topic or subject of the inquiry
        email (StringField): User's email address for response
        body (TextAreaField): Detailed question or message content
        submit (SubmitField): Form submission button
    
    Validation Rules:
        - All fields are required (DataRequired)
        - Subject: Maximum 100 characters
        - Email: Valid email format, maximum 120 characters
        - Body: Maximum 2000 characters to prevent spam
    
    Security Considerations:
        - CSRF protection inherited from FlaskForm
        - Input length limits prevent database overflow
        - Email validation prevents invalid addresses
        - Content length limits reduce spam potential
    """
    
    subject = StringField(
        'Reference Subject', 
        validators=[
            DataRequired(message='Please enter a subject for your inquiry.'),
            Length(max=100, message='Subject must be less than 100 characters.')
        ],
        render_kw={'placeholder': 'Enter the topic of your question...'}
    )
    
    email = StringField(
        'Email Address', 
        validators=[
            DataRequired(message='Please enter your email address.'),
            Email(message='Please enter a valid email address.'),
            Length(max=120, message='Email must be less than 120 characters.')
        ],
        render_kw={'placeholder': 'your.email@example.com'}
    )
    
    body = TextAreaField(
        'Your Question', 
        validators=[
            DataRequired(message='Please enter your question or message.'),
            Length(max=2000, message='Message must be less than 2000 characters.')
        ],
        render_kw={
            'placeholder': 'Please describe your question or issue in detail...',
            'rows': 6
        }
    )
    
    submit = SubmitField('Send Request')