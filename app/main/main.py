from flask import render_template, redirect, url_for
from flask_login import current_user
from app.models import Document, Question # Import Question and Notification models
from . import bp
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

@bp.route('/errore')
def errore():
    """
    Pagina di errore generica per i link del footer.
    """
    return render_template('errors/404.html'), 404

@bp.route('/')
def index():
    """
    StudyHub Homepage
    - Shows landing page for non-authenticated users
    - Redirects to dashboard for authenticated users
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('main/home.html')

@bp.route('/dashboard')
def dashboard():
    """
    User Dashboard
    - Shows personalized dashboard for authenticated users
    - Redirects to login for non-authenticated users
    """
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    
    # Calculate the number of documents uploaded by the current user
    document_count = current_user.documents.count()
    
    # Calculate the number of documents favorited by the current user
    favorite_count = current_user.favorites.count()

    # Calculate the number of documents downloaded by the current user
    downloads_count = current_user.downloads.count()

    # Calculate the number of forms sent by the current user
    forms_sent_count = current_user.questions.count()
    
    return render_template('main/dashboard.html', 
                           document_count=document_count,
                           favorite_count=favorite_count,
                           downloads_count=downloads_count,
                           forms_sent_count=forms_sent_count)