"""
app/upload/__init__.py - Document Upload Blueprint Initialization

This file creates the 'upload' blueprint for document upload functionality.
The upload blueprint handles:
- Document file uploads (PDF, DOC, DOCX, PPT, PPTX)
- Document metadata collection and validation
- File processing and storage
- Upload form handling and validation

Blueprint pattern allows modular organization of upload-related routes.
"""

from flask import Blueprint

# Create the upload blueprint
# This blueprint handles all document upload functionality
bp = Blueprint('upload', __name__)

# Import route handlers and utilities after blueprint creation
# This prevents circular import issues
from app.upload import upload, utils
