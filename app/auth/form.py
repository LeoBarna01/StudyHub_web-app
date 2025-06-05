"""
app/auth/form.py - Authentication Forms

This module defines all forms used in the authentication system using Flask-WTF.
Flask-WTF provides CSRF protection, validation, and form handling capabilities.

Forms included:
- LoginForm: User authentication
- RegistrationForm: New user account creation  
- EditProfileForm: Profile information editing
- UpdateProfileForm: Profile image updates

All forms include proper validation to ensure data integrity and security.
"""

# Import Flask-WTF components for form handling
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed

# Import WTForms field types and validators
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

# Import User model for validation checks
from app.models import User

# ============================================================================
# AUTHENTICATION FORMS
# ============================================================================

class LoginForm(FlaskForm):
    """
    User login form with email and password authentication.
    
    Features:
    - Email validation with proper format checking
    - Password field with secure input (hidden characters)  
    - Optional "Remember Me" checkbox for persistent sessions
    - CSRF protection automatically included by Flask-WTF
    
    Fields:
        email: User's registered email address (required)
        password: User's password (required)
        remember: Checkbox to keep user logged in (optional)
        submit: Submit button to process login
    """
    email = StringField(
        'Email', 
        validators=[
            DataRequired(message='Email address is required'),
            Email(message='Please enter a valid email address')
        ]
    )
    password = PasswordField(
        'Password', 
        validators=[DataRequired(message='Password is required')]
    )
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    """
    New user registration form with comprehensive validation.
    
    Features:
    - Full name collection (first and last name)
    - Email uniqueness validation
    - Password strength requirements
    - Password confirmation matching
    - Automatic CSRF protection
    
    Fields:
        first_name: User's first name (2-50 characters)
        last_name: User's last name (2-50 characters) 
        email: User's email address (unique, validated format)
        password: User's password (minimum 6 characters)
        confirm: Password confirmation (must match password)
        submit: Submit button to create account
    """
    first_name = StringField(
        'First Name', 
        validators=[
            DataRequired(message='First name is required'),
            Length(min=2, max=50, message='First name must be between 2 and 50 characters')
        ]
    )
    last_name = StringField(
        'Last Name', 
        validators=[
            DataRequired(message='Last name is required'),
            Length(min=2, max=50, message='Last name must be between 2 and 50 characters')
        ]
    )
    email = StringField(
        'Email', 
        validators=[
            DataRequired(message='Email address is required'),
            Email(message='Please enter a valid email address')
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(message='Password is required'),
            Length(min=6, message='Password must be at least 6 characters long'),
            EqualTo('confirm', message='Passwords must match')
        ]
    )
    confirm = PasswordField(
        'Confirm Password', 
        validators=[DataRequired(message='Please confirm your password')]
    )
    submit = SubmitField('Register')

    def validate_email(self, email):
        """
        Custom validator to ensure email uniqueness.
        
        This method is automatically called by WTForms during validation.
        It checks if the email address is already registered in the database.
        
        Args:
            email: The email field being validated
            
        Raises:
            ValidationError: If email is already registered
        """
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email address is already registered. Please choose a different one.')


class EditProfileForm(FlaskForm):
    """
    Profile editing form for updating user information.
    
    Features:
    - Optional field updates (user can update only desired fields)
    - Academic information collection
    - Profile image upload with format validation
    - Flexible validation (all fields optional for partial updates)
    
    Fields:
        first_name: Update first name (optional, max 50 characters)
        last_name: Update last name (optional, max 50 characters)
        institute: User's institution/university (optional, max 100 characters)
        course: User's degree program (optional, max 100 characters)
        year: Academic year (optional, max 10 characters)
        profile_image: Profile picture upload (optional, images only)
        submit: Submit button to save changes
    """
    first_name = StringField(
        'First Name', 
        validators=[Length(max=50, message='First name cannot exceed 50 characters')]
    )
    last_name = StringField(
        'Last Name', 
        validators=[Length(max=50, message='Last name cannot exceed 50 characters')]
    )
    institute = StringField(
        'Institution', 
        validators=[Length(max=100, message='Institution name cannot exceed 100 characters')]
    )
    course = StringField(
        'Degree Program', 
        validators=[Length(max=100, message='Degree program cannot exceed 100 characters')]
    )
    year = StringField(
        'Academic Year', 
        validators=[Length(max=10, message='Academic year cannot exceed 10 characters')]
    )
    profile_image = FileField(
        'Update Profile Picture', 
        validators=[
            FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Only image files are allowed (JPG, PNG, JPEG, GIF)')
        ]
    )
    submit = SubmitField('Save Changes')


class UpdateProfileForm(FlaskForm):
    """
    Simplified form specifically for profile image updates.
    
    This form provides a focused interface for users who only want to
    update their profile picture without editing other information.
    
    Features:
    - Image format validation
    - File size handling (managed by Flask configuration)
    - Simple single-purpose interface
    
    Fields:
        profile_image: New profile picture upload (images only)
        submit: Submit button to update profile
    """
    profile_image = FileField(
        'Profile Image', 
        validators=[
            FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Only image files are allowed (JPG, JPEG, PNG, GIF)')
        ]
    )
    submit = SubmitField('Update Profile')