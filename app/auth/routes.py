from flask import (
    render_template, redirect, url_for,
    flash, request, current_app, jsonify
)
from flask_login import (
    current_user, login_user,
    logout_user, login_required
)
from urllib.parse import urlparse
from app import db
from app.auth import bp
from app.auth.form import (
    LoginForm, RegistrationForm,
    EditProfileForm, UpdateProfileForm
)
from app.models import User, Document
from werkzeug.utils import secure_filename
import os
from werkzeug.datastructures import FileStorage
import time
from sqlalchemy.exc import IntegrityError
from PIL import Image

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login. Redirect authenticated users to home."""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            # Prevent open‐redirect
            if not next_page or urlparse(next_page).netloc:
                next_page = url_for('main.index')
            return redirect(next_page)
        flash('Invalid email or password', 'danger')
    return render_template('auth/login.html', form=form)


@bp.route('/logout')
def logout():
    """Log the user out and redirect to the home page."""
    logout_user()
    return redirect(url_for('main.index'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    """Handle new user registration. Redirect to login after success."""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        try:
            db.session.commit()
            flash('Registration successful! You may now sign in.', 'success')
            logout_user()
            return redirect(url_for('auth.login'))
        except IntegrityError:
            db.session.rollback()
            flash('This email address is already registered. Please <a href="{}">Login</a>.'.format(url_for('auth.login')), 'warning')
            return render_template('auth/register.html', form=form)

    return render_template('auth/register.html', form=form)


@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """
    Display and allow edits to the current user's profile.
    Also load their uploads and favorites for listing.
    """
    form = UpdateProfileForm()
    
    # Configure upload folder in the project root's static directory
    upload_folder = os.path.join(current_app.root_path, '..', 'static', 'profile_pics')
    # Ensure the upload folder exists
    os.makedirs(upload_folder, exist_ok=True)

    if form.validate_on_submit():
        # Handle profile image upload
        if form.profile_image.data:
            if isinstance(form.profile_image.data, FileStorage):
                try:
                    image_file = form.profile_image.data
                    filename = secure_filename(image_file.filename)
                    
                    if not '.' in filename:
                        flash('Invalid image file format', 'danger')
                        return redirect(url_for('auth.profile'))
                    
                    allowed_extensions = {'jpg', 'jpeg', 'png', 'gif'}
                    if not filename.rsplit('.', 1)[1].lower() in allowed_extensions:
                         flash('Invalid image file format', 'danger')
                         return redirect(url_for('auth.profile'))

                    # Generate unique filename
                    unique_filename = f"{current_user.id}_{int(time.time())}_{filename}"
                    
                    # Define the path to save the original image temporarily (optional but good practice)
                    temp_original_path = os.path.join(upload_folder, 'temp_' + unique_filename)
                    image_file.save(temp_original_path)

                    # --- Image Processing (Cropping and Resizing) --- 
                    # Assuming frontend sends crop coordinates (example: x, y, width, height)
                    # In a real app, you would get these from request.form or request.json
                    # For demonstration, let's assume some dummy crop coordinates or process the center
                    
                    try:
                        img = Image.open(temp_original_path)

                        # Example Cropping Logic: Crop a square from the center
                        # This assumes you want the center of the image.
                        # For actual user-defined cropping, you'd use coords from frontend.
                        width, height = img.size
                        min_dim = min(width, height)
                        left = (width - min_dim) / 2
                        top = (height - min_dim) / 2
                        right = (width + min_dim) / 2
                        bottom = (height + min_dim) / 2
                        
                        # Crop the center square
                        img_cropped = img.crop((left, top, right, bottom))
                        
                        # Resize to profile picture size (e.g., 150x150)
                        output_size = (150, 150)
                        img_resized = img_cropped.resize(output_size, Image.Resampling.LANCZOS)
                        
                        # Define the final save path
                        final_save_path = os.path.join(upload_folder, unique_filename)
                        
                        # Save the processed image
                        img_resized.save(final_save_path)
                        
                        # Remove the temporary original file
                        os.remove(temp_original_path)
                        
                    except Exception as img_e:
                         flash(f'An error occurred during image processing: {img_e}', 'danger')
                         current_app.logger.error(f'Error processing image: {img_e}')
                         # Clean up temporary file if it exists
                         if os.path.exists(temp_original_path):
                             os.remove(temp_original_path)
                         return redirect(url_for('auth.profile'))
                    # --- End Image Processing ---

                    # Update user's profile image path in the database
                    current_user.profile_image = unique_filename
                    db.session.commit()

                    flash('Your profile image has been updated!', 'success')
                    return redirect(url_for('auth.profile'))
                except Exception as e:
                    db.session.rollback() # Rollback database changes if any occurred before image processing
                    flash(f'An error occurred while uploading the image: {e}', 'danger')
                    current_app.logger.error(f'Error uploading image: {e}')
                    # Ensure temporary file is removed even if upload fails early
                    temp_original_path = os.path.join(upload_folder, 'temp_' + secure_filename(form.profile_image.data.filename))
                    if os.path.exists(temp_original_path):
                         os.remove(temp_original_path)
                    return redirect(url_for('auth.profile'))
            else:
                 flash('Invalid file data provided.', 'danger')
                 return redirect(url_for('auth.profile'))

    # Determine the correct image URL to display
    image_file = url_for('static', filename='profile_pics/' + (current_user.profile_image if current_user.profile_image else 'default_avatar.jpg'))
    
    # Load user's uploaded documents
    user_uploads = current_user.documents.all()

    # Load user's favorited documents
    user_favorites = current_user.favorites.all()

    return render_template(
        'auth/profile.html',
        title='Profile',
        form=form,
        image_file=image_file,
        my_uploads=user_uploads, # Pass uploaded documents
        favorites=user_favorites # Pass favorited documents
    )


# Function to save resized image (Optional, but recommended for efficiency)
def save_picture(form_picture):
    # ... existing code if you have it ...
    pass # Placeholder if you have this function elsewhere or need to implement it


# You might also need to adjust how the image is displayed in the template.
# Make sure the template uses url_for('static', filename='profile_pics/' + user.profile_image) to get the image URL.

@bp.route('/api/profile_image', methods=['GET'])
@login_required
def get_profile_image():
    image_url = url_for('static', filename='profile_pics/' + (current_user.profile_image if current_user.profile_image else 'default_avatar.jpg'))
    return jsonify({'image_url': image_url})