"""
app/main/main.py - Main Application Routes

This module contains the core routes for the StudyHub application:
- Index route: Landing page for non-authenticated users
- Dashboard route: Personalized dashboard for authenticated users
- Error route: Generic error page for footer links

The routes handle user authentication flow and display appropriate content
based on authentication status.
"""

# Import Flask utilities and extensions
from flask import render_template, redirect, url_for
from flask_login import current_user

# Import database models
from app.models import Document, Question

# Import the blueprint instance
from . import bp

# Remove unused import
# from flask_sqlalchemy import SQLAlchemy
# db = SQLAlchemy()  # This is redundant - db is already initialized in __init__.py

# ============================================================================
# ROUTE HANDLERS
# ============================================================================

@bp.route('/error')
def error():
    """
    Generic error page for footer links.
    
    This route serves a 404 error page for placeholder links in the footer
    that don't have actual functionality implemented yet.
    
    Returns:
        Rendered 404 error template with 404 status code
    """
    return render_template('errors/404.html'), 404


@bp.route('/')
def index():
    """
    StudyHub Homepage - Application entry point.
    
    This route serves different content based on user authentication status:
    - Non-authenticated users: Landing page with app description and auth links
    - Authenticated users: Redirect to personalized dashboard
    
    Returns:
        For non-authenticated: Landing page template
        For authenticated: Redirect to dashboard
    """
    if current_user.is_authenticated:
        # User is logged in - redirect to their personalized dashboard
        return redirect(url_for('main.dashboard'))
    
    # User is not logged in - show the landing/home page
    return render_template('main/home.html')


@bp.route('/dashboard')
def dashboard():
    """
    User Dashboard - Personalized user homepage.
    
    This route displays a personalized dashboard with user statistics:
    - Number of documents uploaded by the user
    - Number of documents marked as favorites
    - Number of documents downloaded
    - Number of support forms submitted
    
    Access Control:
        Only authenticated users can access this page.
        Non-authenticated users are redirected to login.
    
    Returns:
        Dashboard template with user statistics
        OR redirect to login for non-authenticated users
    """
    if not current_user.is_authenticated:
        # User is not logged in - redirect to login page
        return redirect(url_for('auth.login'))
    
    # ========================================================================
    # CALCULATE USER STATISTICS
    # ========================================================================
    
    # Count documents uploaded by the current user
    # Uses the relationship defined in User model: documents = db.relationship('Document', ...)
    document_count = current_user.documents.count()
    
    # Count documents favorited by the current user
    # Uses the many-to-many relationship: favorites = db.relationship('Document', secondary=user_favorites, ...)
    favorite_count = current_user.favorites.count()

    # Count documents downloaded by the current user
    # Uses the many-to-many relationship: downloads = db.relationship('Document', secondary=user_downloads, ...)
    downloads_count = current_user.downloads.count()

    # Count support forms/questions sent by the current user
    # Uses the relationship: questions = db.relationship('Question', ...)
    forms_sent_count = current_user.questions.count()
    
    # Render the dashboard template with all calculated statistics
    return render_template('main/dashboard.html', 
                           document_count=document_count,
                           favorite_count=favorite_count,
                           downloads_count=downloads_count,
                           forms_sent_count=forms_sent_count)