"""
StudyHub Contact Form Routes

This module handles the routing and processing logic for contact forms
and support requests. It manages form rendering, validation, database
storage, and user feedback.

Routes:
    - GET /form/form: Display the contact form
    - POST /form/form: Process form submission

Features:
    - Form validation and error handling
    - Database storage of all submissions
    - Success/error message feedback
    - Optional email notification system
    - Redirect after successful submission (PRG pattern)

Security Features:
    - CSRF protection via FlaskForm
    - Input validation and sanitization
    - Database transaction handling
    - Error logging and monitoring

Author: StudyHub Development Team
License: MIT
"""

# =============================================================================
# CORE IMPORTS
# =============================================================================

# Flask framework components
from flask import render_template, flash, redirect, url_for, request

# Database and application imports
from app import db
from app.form import bp
from app.form.forms import QuestionForm
from app.models import Question

# =============================================================================
# CONTACT FORM ROUTES
# =============================================================================

@bp.route('/form', methods=['GET', 'POST'])
def ask_question():
    """
    Handle contact form display and submission.
    
    This route implements the Post-Redirect-Get (PRG) pattern to prevent
    duplicate form submissions and provides a clean user experience.
    
    GET Request:
        - Renders the contact form template
        - Provides empty form for user input
        - Displays any flash messages from previous submissions
    
    POST Request:
        - Validates form input using WTForms validators
        - Creates new Question model instance
        - Saves submission to database
        - Sends success message to user
        - Redirects to prevent duplicate submissions
        - Handles validation errors gracefully
    
    Returns:
        GET: Rendered template with form
        POST (success): Redirect to same route with success message
        POST (validation error): Rendered template with error messages
    
    Database Operations:
        - Creates new Question record
        - Commits transaction to database
        - Handles database errors gracefully
    
    Security Considerations:
        - CSRF protection from FlaskForm
        - Input validation prevents malicious data
        - Database transactions ensure data integrity
        - Error handling prevents information disclosure
    
    Future Enhancements:
        - Email notification to administrators
        - Rate limiting to prevent spam
        - Captcha integration for additional security
        - File attachment support for detailed reports
    """
    
    # Initialize the contact form
    form = QuestionForm()
    
    # Process form submission (POST request)
    if form.validate_on_submit():
        try:
            # Create new question record from form data
            question = Question(
                subject=form.subject.data.strip(),  # Remove whitespace
                email=form.email.data.strip().lower(),  # Normalize email
                body=form.body.data.strip()  # Remove whitespace
            )
            
            # Save to database
            db.session.add(question)
            db.session.commit()
            
            # TODO: Optional email notification to administrators
            # send_notification_email(question)
            
            # Provide success feedback to user
            flash('Your request has been submitted successfully. We will respond to your email soon.', 'success')
            
            # Redirect to prevent duplicate submissions (PRG pattern)
            return redirect(url_for('form.ask_question'))
            
        except Exception as e:
            # Handle database errors gracefully
            db.session.rollback()
            flash('An error occurred while submitting your request. Please try again.', 'error')
            
            # Log error for debugging (in production, use proper logging)
            print(f"Contact form error: {e}")
    
    # Render form template (GET request or validation failure)
    return render_template('form/question_form.html', 
                         title='Contact Us',
                         form=form)