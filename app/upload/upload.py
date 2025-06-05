"""
app/upload/upload.py - Document Upload Routes

This module handles document upload functionality for the StudyHub application.
It provides routes for:
- Document file uploads with metadata
- File validation and security checks
- Database integration for document records
- Category and tag management
- File storage and organization

Features:
- Secure file upload handling
- Comprehensive metadata collection
- Dynamic category and tag creation
- Error handling and user feedback
- File organization in upload directories
"""

# Import standard library modules
import os

# Import Flask components
from flask import (
    render_template, request, redirect, url_for, 
    flash, current_app
)

# Import Flask-Login for authentication
from flask_login import login_required, current_user

# Import Werkzeug utilities for file handling
from werkzeug.utils import secure_filename

# Import application components
from app import db
from . import bp
from app.upload.utils import allowed_file
from app.models import Document, Category, Tag
from app.upload.forms import UploadDocumentForm

# ============================================================================
# DOCUMENT UPLOAD ROUTES
# ============================================================================

@bp.route('/', methods=['GET', 'POST'])
@login_required
def upload_document():
    """
    Handle document upload requests with comprehensive processing.
    
    This route manages the complete document upload workflow:
    - Display upload form for GET requests
    - Process file uploads and metadata for POST requests
    - Validate uploaded files for security
    - Create database records with relationships
    - Handle categories and tags dynamically
    
    Features:
    - Secure file validation and storage
    - Automatic directory creation
    - Dynamic category and tag management
    - Comprehensive error handling
    - User feedback for all operations
    - Database transaction management
    
    Access Control:
        Requires user authentication (@login_required)
    
    GET: Display upload form with instructions
    POST: Process uploaded file and create document record
    
    Returns:
        GET: Upload template with form
        POST: Redirect to upload page on success,
              upload template with errors on failure
    """
    # Initialize upload form
    form = UploadDocumentForm()
    
    # Process form submission
    if form.validate_on_submit():
        # ====================================================================
        # EXTRACT AND VALIDATE FORM DATA
        # ====================================================================
        
        # Extract form data
        title = form.title.data
        description = form.description.data
        institute = form.institute.data
        course = form.course.data
        subject = form.subject.data
        category_name = form.category.data
        tags_string = form.tags.data
        file = form.file.data

        # ====================================================================
        # FILE VALIDATION AND STORAGE
        # ====================================================================
        
        # Validate uploaded file exists and has allowed extension
        if file and allowed_file(file.filename):
            # Secure the filename to prevent directory traversal attacks
            filename = secure_filename(file.filename)
            
            # Configure upload directories
            upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
            documents_folder = os.path.join(upload_folder, 'documents')
            
            # Ensure documents upload directory exists
            full_documents_path = os.path.join(current_app.root_path, documents_folder)
            os.makedirs(full_documents_path, exist_ok=True)
            
            # Define complete file path for storage
            file_path = os.path.join(full_documents_path, filename)
            
            # Save uploaded file to server
            file.save(file_path)

            # ================================================================
            # CREATE DOCUMENT DATABASE RECORD
            # ================================================================
            
            # Create new Document instance with form data
            doc = Document(
                title=title,
                description=description,
                institute=institute,
                course=course,
                subject=subject,
                # Store relative path with subdirectory for proper serving
                filename=os.path.join('documents', filename),
                author=current_user  # Automatically set to current user
                # category and tags will be handled separately below
            )

            # ================================================================
            # HANDLE CATEGORY MANAGEMENT
            # ================================================================
            
            # Process optional category
            if category_name:
                # Check if category already exists
                category = Category.query.filter_by(name=category_name).first()
                if not category:
                    # Create new category if it doesn't exist
                    category = Category(name=category_name)
                    db.session.add(category)
                # Associate category with document
                doc.category = category

            # ================================================================
            # HANDLE TAG MANAGEMENT
            # ================================================================
            
            # Process comma-separated tags
            if tags_string:
                # Split tags by comma and process each one
                for tag_name in tags_string.split(','):
                    tag_name = tag_name.strip()  # Remove whitespace
                    if not tag_name:  # Skip empty tags
                        continue
                    
                    # Check if tag already exists
                    tag = Tag.query.filter_by(name=tag_name).first()
                    if not tag:
                        # Create new tag if it doesn't exist
                        tag = Tag(name=tag_name)
                        db.session.add(tag)
                    
                    # Associate tag with document (many-to-many relationship)
                    doc.tags.append(tag)

            # ================================================================
            # DATABASE COMMIT AND SUCCESS HANDLING
            # ================================================================
            
            # Add document to database session
            db.session.add(doc)
            
            try:
                # Commit all changes to database
                db.session.commit()
                flash('Document uploaded successfully!', 'success')
                
                # Redirect to prevent duplicate submissions on page refresh
                return redirect(url_for('upload.upload_document'))
                
            except Exception as e:
                # Handle database errors
                db.session.rollback()
                flash(f'An error occurred while saving the document: {e}', 'danger')
                current_app.logger.error(f'Database error during upload: {e}')
                
                # Optionally remove uploaded file if database save failed
                try:
                    os.remove(file_path)
                except OSError:
                    pass  # File removal failed, but not critical
        else:
            # File validation failed
            flash('Invalid file format. Allowed formats: PDF, DOC, DOCX, PPT, PPTX.', 'danger')

    # Render upload page for GET requests or after form validation failure
    return render_template('upload/upload.html', form=form)