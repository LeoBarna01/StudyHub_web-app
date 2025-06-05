"""
app/auth/routes.py - Authentication and Profile Management Routes

This module handles all authentication-related routes for the StudyHub application:
- User login and logout functionality
- User registration with validation
- Profile management and editing
- Profile image upload and processing
- Secure file serving for profile pictures

Features:
- Secure password hashing and verification
- Image processing with PIL for profile pictures  
- File upload validation and security
- Session management with Flask-Login
- Error handling and user feedback
"""

# Import Flask core components
from flask import (
    render_template, redirect, url_for, flash, request, 
    current_app, jsonify, send_from_directory
)

# Import Flask-Login components for authentication
from flask_login import (
    current_user, login_user, logout_user, login_required
)

# Import additional utilities
from urllib.parse import urlparse
import os
import time
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from sqlalchemy.exc import IntegrityError
from PIL import Image

# Import application components
from app import db
from app.auth import bp
from app.auth.form import (
    LoginForm, RegistrationForm, EditProfileForm, UpdateProfileForm
)
from app.models import User, Document

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def allowed_file(filename):
    """
    Check if uploaded file has an allowed image extension.
    
    This function validates file extensions to ensure only image files
    are uploaded for profile pictures, enhancing security.
    
    Args:
        filename (str): Name of the uploaded file
        
    Returns:
        bool: True if file extension is allowed, False otherwise
    """
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

# ============================================================================
# AUTHENTICATION ROUTES
# ============================================================================

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle user login with email and password authentication.
    
    This route processes user login requests and manages session creation.
    It includes security features like redirect validation and proper
    session management.
    
    GET: Display login form
    POST: Process login credentials and create user session
    
    Security Features:
    - Validates user credentials against database
    - Prevents open redirect attacks
    - Supports "Remember Me" functionality
    - Proper session management
    
    Returns:
        GET: Login template with form
        POST: Redirect to intended page or dashboard on success,
              login template with errors on failure
    """
    # Redirect authenticated users to prevent unnecessary login attempts
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    # Create and process login form
    form = LoginForm()
    if form.validate_on_submit():
        # Query user by email address
        user = User.query.filter_by(email=form.email.data).first()
        
        # Verify user exists and password is correct
        if user and user.check_password(form.password.data):
            # Log in the user with optional "remember me" functionality
            login_user(user, remember=form.remember.data)
            
            # Handle redirect to originally requested page
            next_page = request.args.get('next')
            
            # Security check: prevent open redirect attacks
            # Only allow redirects to same-origin URLs
            if not next_page or urlparse(next_page).netloc:
                next_page = url_for('main.index')
            
            return redirect(next_page)
        
        # Login failed - display error message
        flash('Invalid email or password', 'danger')
    
    return render_template('auth/login.html', form=form)


@bp.route('/logout')
def logout():
    """
    Log out the current user and clear their session.
    
    This route handles user logout by clearing the session data
    and redirecting to the homepage.
    
    Returns:
        Redirect to main index page
    """
    logout_user()
    return redirect(url_for('main.index'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle new user registration with comprehensive validation.
    
    This route processes new user account creation with proper
    validation, error handling, and database integrity checks.
    
    GET: Display registration form
    POST: Process registration data and create new user account
    
    Features:
    - Form validation (email format, password strength, etc.)
    - Email uniqueness validation
    - Secure password hashing
    - Database integrity error handling
    - User feedback for success/failure
    
    Returns:
        GET: Registration template with form
        POST: Redirect to login on success,
              registration template with errors on failure
    """
    # Redirect authenticated users to prevent duplicate accounts
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    # Create and process registration form
    form = RegistrationForm()
    if form.validate_on_submit():
        # Create new user instance with form data
        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data
        )
        
        # Set password using secure hashing
        user.set_password(form.password.data)
        
        # Add user to database with error handling
        db.session.add(user)
        try:
            db.session.commit()
            flash('Registration successful! You may now sign in.', 'success')
            
            # Ensure user is logged out (just in case)
            logout_user()
            return redirect(url_for('auth.login'))
            
        except IntegrityError:
            # Handle database constraint violations (e.g., duplicate email)
            db.session.rollback()
            flash(
                'This email address is already registered. Please <a href="{}">Login</a>.'.format(
                    url_for('auth.login')
                ), 
                'warning'
            )
            return render_template('auth/register.html', form=form)

    return render_template('auth/register.html', form=form)


# ============================================================================
# PROFILE MANAGEMENT ROUTES
# ============================================================================

@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """
    Display and manage user profile information and settings.
    
    This route provides comprehensive profile management functionality:
    - Display current user information
    - Handle profile image uploads with processing
    - Show user's uploaded documents
    - Show user's favorite documents
    - Image processing (cropping, resizing) for profile pictures
    
    Features:
    - Secure file upload handling
    - Image processing with PIL (cropping and resizing)
    - Error handling for image processing failures
    - Database transaction management
    - User feedback for all operations
    
    GET: Display profile page with user info and documents
    POST: Process profile image updates
    
    Returns:
        Profile template with user data, documents, and form
    """
    # Initialize profile update form
    form = UpdateProfileForm()
    
    # Configure upload directory for profile images
    upload_folder = os.path.join(current_app.root_path, '..', 'uploads', 'profile_pics')
    # Ensure upload directory exists
    os.makedirs(upload_folder, exist_ok=True)

    # Handle form submission (profile image upload)
    if form.validate_on_submit():
        # Process profile image upload
        if form.profile_image.data:
            # Validate that uploaded data is a proper file
            if isinstance(form.profile_image.data, FileStorage):
                try:
                    image_file = form.profile_image.data
                    filename = secure_filename(image_file.filename)
                    
                    # Additional validation for file format
                    if not '.' in filename:
                        flash('Invalid image file format', 'danger')
                        return redirect(url_for('auth.profile'))
                    
                    # Check file extension
                    allowed_extensions = {'jpg', 'jpeg', 'png', 'gif'}
                    if not filename.rsplit('.', 1)[1].lower() in allowed_extensions:
                         flash('Invalid image file format', 'danger')
                         return redirect(url_for('auth.profile'))

                    # Generate unique filename to prevent conflicts
                    unique_filename = f"{current_user.id}_{int(time.time())}_{filename}"
                    
                    # Create temporary path for original image processing
                    temp_original_path = os.path.join(upload_folder, 'temp_' + unique_filename)
                    image_file.save(temp_original_path)

                    # ================================================================
                    # IMAGE PROCESSING: CROPPING AND RESIZING
                    # ================================================================
                    
                    try:
                        # Open the uploaded image for processing
                        img = Image.open(temp_original_path)

                        # Example Cropping Logic: Create square crop from center
                        # In a production app, crop coordinates would come from frontend
                        # This ensures profile pictures are consistently square
                        width, height = img.size
                        min_dim = min(width, height)
                        
                        # Calculate center crop coordinates
                        left = (width - min_dim) / 2
                        top = (height - min_dim) / 2
                        right = (width + min_dim) / 2
                        bottom = (height + min_dim) / 2
                        
                        # Crop to square from center
                        img_cropped = img.crop((left, top, right, bottom))
                        
                        # Resize to standard profile picture size (150x150 pixels)
                        output_size = (150, 150)
                        img_resized = img_cropped.resize(output_size, Image.Resampling.LANCZOS)
                        
                        # Define final save path for processed image
                        final_save_path = os.path.join(upload_folder, unique_filename)
                        
                        # Save the processed image
                        img_resized.save(final_save_path)
                        
                        # Clean up: remove temporary original file
                        os.remove(temp_original_path)
                        
                    except Exception as img_e:
                        # Handle image processing errors
                        flash(f'An error occurred during image processing: {img_e}', 'danger')
                        current_app.logger.error(f'Error processing image: {img_e}')
                        
                        # Clean up temporary file if it exists
                        if os.path.exists(temp_original_path):
                            os.remove(temp_original_path)
                        return redirect(url_for('auth.profile'))
                    
                    # ================================================================
                    # DATABASE UPDATE
                    # ================================================================

                    # Update user's profile image path in database
                    current_user.profile_image = unique_filename
                    db.session.commit()

                    flash('Your profile image has been updated!', 'success')
                    return redirect(url_for('auth.profile'))
                    
                except Exception as e:
                    # Handle general upload errors
                    db.session.rollback()  # Rollback any database changes
                    flash(f'An error occurred while uploading the image: {e}', 'danger')
                    current_app.logger.error(f'Error uploading image: {e}')
                    
                    # Ensure temporary file cleanup
                    if 'temp_original_path' in locals() and os.path.exists(temp_original_path):
                        os.remove(temp_original_path)
                    return redirect(url_for('auth.profile'))
            else:
                # Invalid file data provided
                flash('Invalid file data provided.', 'danger')
                return redirect(url_for('auth.profile'))

    # ========================================================================
    # PREPARE DATA FOR TEMPLATE RENDERING
    # ========================================================================

    # Determine correct profile image URL for display
    if current_user.profile_image:
        # User has uploaded a custom image - serve from uploads
        image_file = url_for('auth.profile_pic', filename=current_user.profile_image)
    else:
        # Use default avatar from static assets
        image_file = url_for('static', filename='profile_pics/default_avatar.jpg')
    
    # Load user's uploaded documents for display
    user_uploads = current_user.documents.all()

    # Load user's favorited documents for display
    user_favorites = current_user.favorites.all()

    # Render profile template with all necessary data
    return render_template(
        'auth/profile.html',
        title='Profile',
        form=form,
        image_file=image_file,
        my_uploads=user_uploads,     # Pass uploaded documents
        favorites=user_favorites     # Pass favorited documents
    )

# ============================================================================
# UTILITY FUNCTIONS (LEGACY - PLACEHOLDER)
# ============================================================================

def save_picture(form_picture):
    """
    Legacy function placeholder for image processing.
    
    This function exists for compatibility but is not currently used.
    Image processing is handled directly in the profile() route.
    Can be implemented for additional image processing needs.
    
    Args:
        form_picture: Uploaded image file from form
        
    Returns:
        None: Currently a placeholder function
    """
    # Placeholder implementation - image processing handled in profile() route
    pass

# ============================================================================
# API ENDPOINTS
# ============================================================================

@bp.route('/api/profile_image', methods=['GET'])
@login_required
def get_profile_image():
    """
    API endpoint to get current user's profile image URL.
    
    This endpoint provides a JSON response with the user's current
    profile image URL, useful for AJAX requests and dynamic updates.
    
    Access Control:
        Requires user authentication
    
    Returns:
        JSON response with image_url field containing the profile image URL
    """
    # Determine appropriate image URL (custom or default)
    if current_user.profile_image:
        image_url = url_for('auth.profile_pic', filename=current_user.profile_image)
    else:
        image_url = url_for('static', filename='profile_pics/default_avatar.jpg')
    
    return jsonify({'image_url': image_url})

# ============================================================================
# FILE SERVING ROUTES
# ============================================================================

@bp.route('/uploads/profile_pics/<path:filename>', methods=['GET'])
@login_required
def send_profile_image(filename):
    """
    Legacy route for serving profile images from uploads folder.
    
    This route provides backward compatibility but the preferred
    route is 'profile_pic' which has better security and organization.
    
    Args:
        filename: Name of the image file to serve
        
    Returns:
        File response with the requested image
    """
    uploads_folder = os.path.join(current_app.root_path, '..', 'uploads', 'profile_pics')
    return send_from_directory(uploads_folder, filename)


@bp.route('/profile_pic/<filename>')
def profile_pic(filename):
    """
    Serve profile pictures from the uploads directory.
    
    This route securely serves uploaded profile pictures while maintaining
    proper file access controls and error handling.
    
    Features:
    - Secure file serving from uploads directory
    - Proper path handling to prevent directory traversal
    - Error handling for missing files
    
    Args:
        filename: Name of the profile picture file to serve
        
    Returns:
        File response with the requested profile picture
        or 404 if file doesn't exist
    """
    # Define secure path to uploads folder
    uploads_folder = os.path.join(current_app.root_path, '..', 'uploads', 'profile_pics')
    
    # Serve file with built-in security checks
    return send_from_directory(uploads_folder, filename)