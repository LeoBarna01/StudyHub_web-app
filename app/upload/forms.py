"""
app/upload/forms.py - Document Upload Forms

This module defines forms for document upload functionality using Flask-WTF.
These forms handle document metadata collection and file uploads with
proper validation to ensure data integrity and file security.

Forms included:
- UploadDocumentForm: Complete document upload with metadata

All forms include CSRF protection and comprehensive validation.
"""

# Import Flask-WTF components for form handling
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed

# Import WTForms field types and validators
from wtforms import StringField, TextAreaField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length

# ============================================================================
# DOCUMENT UPLOAD FORMS
# ============================================================================

class UploadDocumentForm(FlaskForm):
    """
    Form for uploading new documents with comprehensive metadata.
    
    This form collects all necessary information about a document
    including academic context, descriptive information, and the file itself.
    
    Features:
    - Document metadata collection
    - Academic context information (institute, course, subject)
    - Categorization and tagging system
    - File upload with format validation
    - Comprehensive field validation
    
    Fields:
        title: Document title (required, max 200 characters)
        institute: Academic institution (optional, max 200 characters)
        year: Academic year (optional, max 50 characters, flexible format)
        course: Academic course/program (optional, max 200 characters)
        subject: Subject/topic area (optional, max 200 characters)
        description: Brief document description (optional, text area)
        category: Document category (optional, max 100 characters)
        tags: Comma-separated tags (optional, max 200 characters)
        file: Document file upload (required, specific formats only)
        submit: Submit button to upload document
        
    Note:
        - Author is automatically set to current logged-in user
        - File format restrictions are enforced for security
        - Year field is StringField for flexibility (e.g., "2023-2024")
    """
    
    title = StringField(
        'Document Title', 
        validators=[
            DataRequired(message='Document title is required'),
            Length(max=200, message='Title cannot exceed 200 characters')
        ]
    )
    
    institute = StringField(
        'Academic Institute', 
        validators=[
            Length(max=200, message='Institute name cannot exceed 200 characters')
        ]
    )
    
    # Using StringField instead of IntegerField for flexibility
    # Allows formats like "2023-2024", "Fall 2023", etc.
    year = StringField(
        'Academic Year', 
        validators=[
            Length(max=50, message='Academic year cannot exceed 50 characters')
        ]
    )
    
    course = StringField(
        'Academic Course', 
        validators=[
            Length(max=200, message='Course name cannot exceed 200 characters')
        ]
    )
    
    subject = StringField(
        'Subject', 
        validators=[
            Length(max=200, message='Subject cannot exceed 200 characters')
        ]
    )
    
    description = TextAreaField(
        'Brief description of the document',
        validators=[
            Length(max=1000, message='Description cannot exceed 1000 characters')
        ]
    )
    
    category = StringField(
        'Category', 
        validators=[
            Length(max=100, message='Category cannot exceed 100 characters')
        ]
    )
    
    tags = StringField(
        'Tags (comma-separated)', 
        validators=[
            Length(max=200, message='Tags cannot exceed 200 characters')
        ]
    )
    
    file = FileField(
        'Select Document', 
        validators=[
            DataRequired(message='Please select a document to upload'),
            FileAllowed(
                ['pdf', 'doc', 'docx', 'ppt', 'pptx'], 
                'Only document files are allowed (PDF, DOC, DOCX, PPT, PPTX)'
            )
        ]
    )
    
    submit = SubmitField('Upload Document') 