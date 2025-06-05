"""
app/upload/utils.py - Upload Utility Functions

This module provides utility functions for document upload operations.
It includes file validation, security checks, and helper functions
used throughout the upload process.

Functions:
- allowed_file: Validates document file extensions for security
- Additional utility functions can be added here as needed

Security Features:
- File extension validation to prevent malicious uploads
- Configurable allowed file types
- Case-insensitive extension checking
"""

import os

# ============================================================================
# CONFIGURATION
# ============================================================================

# Define allowed file extensions for document uploads
# These extensions are considered safe for academic document sharing
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'ppt', 'pptx'}

# ============================================================================
# FILE VALIDATION FUNCTIONS
# ============================================================================

def allowed_file(filename):
    """
    Validate if uploaded file has an allowed document extension.
    
    This function checks if the uploaded file has an extension that
    is permitted for document uploads. It enhances security by preventing
    upload of potentially dangerous file types.
    
    Security Features:
    - Only allows predefined safe document formats
    - Case-insensitive extension checking
    - Requires files to have an extension
    
    Args:
        filename (str): Name of the uploaded file
        
    Returns:
        bool: True if file extension is allowed, False otherwise
        
    Examples:
        >>> allowed_file('document.pdf')
        True
        >>> allowed_file('presentation.PPTX')
        True
        >>> allowed_file('malicious.exe')
        False
        >>> allowed_file('no_extension')
        False
    """
    return (
        '.' in filename 
        and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    )