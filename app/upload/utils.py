import os

# Allowed file extensions for uploads
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'ppt', 'pptx'}

def allowed_file(filename):
    """
    Check if the uploaded file has an allowed extension.
    Returns True if the extension is allowed, False otherwise.
    """
    return (
        '.' in filename
        and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    )