"""
StudyHub Cloudinary Integration Example

This file provides a complete example implementation for integrating Cloudinary
cloud storage with the StudyHub application. Cloudinary offers powerful image
and file management capabilities for production deployments.

Features:
    - Cloud-based file storage (eliminates local file management)
    - Automatic image optimization and transformation
    - CDN delivery for improved performance
    - Scalable storage solution for production
    - Advanced image processing capabilities

Integration Benefits:
    - Reduced server storage requirements
    - Improved application performance
    - Automatic backups and redundancy
    - Global CDN for fast file delivery
    - Image optimization for web delivery

Setup Instructions:
    1. Create account at cloudinary.com
    2. Get API credentials from dashboard
    3. Set environment variables for security
    4. Install cloudinary package: pip install cloudinary
    5. Update configuration and model files

Security Notes:
    - Store API credentials as environment variables
    - Never commit API keys to version control
    - Use signed URLs for sensitive content
    - Implement proper access controls

Author: StudyHub Development Team
License: MIT
"""

# =============================================================================
# CLOUDINARY PACKAGE IMPORTS
# =============================================================================

import cloudinary  # Core Cloudinary functionality
import cloudinary.uploader  # File upload capabilities
from cloudinary.utils import cloudinary_url  # URL generation utilities
import time  # For unique filename generation

# =============================================================================
# ENHANCED CONFIGURATION CLASS
# =============================================================================

class Config:
    """
    Enhanced configuration class with Cloudinary integration.
    
    Add these settings to your main config.py file to enable
    cloud storage functionality in your StudyHub application.
    """
    
    # ...existing configuration...
    
    # =============================================================================
    # CLOUDINARY CLOUD STORAGE CONFIGURATION
    # =============================================================================
    
    # Cloudinary account credentials
    # IMPORTANT: Set these as environment variables for security
    CLOUDINARY_CLOUD_NAME = os.environ.get('CLOUDINARY_CLOUD_NAME') or 'your_cloud_name'
    CLOUDINARY_API_KEY = os.environ.get('CLOUDINARY_API_KEY') or 'your_api_key'
    CLOUDINARY_API_SECRET = os.environ.get('CLOUDINARY_API_SECRET') or 'your_api_secret'
    
    # Storage preferences
    USE_CLOUDINARY = os.environ.get('USE_CLOUDINARY', 'False').lower() == 'true'
    
    # File organization settings
    CLOUDINARY_FOLDER_PROFILES = 'studyhub/profile_pics'
    CLOUDINARY_FOLDER_DOCUMENTS = 'studyhub/documents'

# =============================================================================
# CLOUDINARY INITIALIZATION
# =============================================================================

def configure_cloudinary():
    """
    Initialize Cloudinary with application credentials.
    
    This function should be called during application startup
    to configure the Cloudinary SDK with your account settings.
    """
    cloudinary.config(
        cloud_name=Config.CLOUDINARY_CLOUD_NAME,
        api_key=Config.CLOUDINARY_API_KEY,
        api_secret=Config.CLOUDINARY_API_SECRET,
        secure=True  # Always use HTTPS
    )

# =============================================================================
# PROFILE IMAGE UPLOAD UTILITIES
# =============================================================================

def upload_profile_image_to_cloudinary(image_file, user_id):
    """
    Upload user profile image to Cloudinary with optimization.
    
    This function handles profile image uploads with automatic
    resizing, optimization, and organized storage.
    
    Args:
        image_file: File object or file path to upload
        user_id (int): User ID for organizing uploads
        
    Returns:
        str: Secure HTTPS URL of uploaded image, or None if error
        
    Features:
        - Automatic resizing to 150x150 pixels
        - Quality optimization for web delivery
        - Organized folder structure
        - Unique filename generation
        - Error handling and logging
    """
    try:
        # Generate unique public ID for the image
        public_id = f"user_{user_id}_{int(time.time())}"
        
        # Upload with transformations and optimizations
        upload_result = cloudinary.uploader.upload(
            image_file,
            folder=Config.CLOUDINARY_FOLDER_PROFILES,
            public_id=public_id,
            transformation=[
                {
                    'width': 150, 
                    'height': 150, 
                    'crop': 'fill',  # Crop to exact dimensions
                    'gravity': 'face'  # Focus on faces when cropping
                },
                {
                    'quality': 'auto',  # Automatic quality optimization
                    'format': 'auto'    # Automatic format selection (WebP, etc.)
                }
            ],
            tags=['profile_image', 'user_content']  # For organization
        )
        
        return upload_result['secure_url']
        
    except Exception as e:
        print(f"❌ Error uploading profile image to Cloudinary: {e}")
        return None

# =============================================================================
# DOCUMENT UPLOAD UTILITIES
# =============================================================================

def upload_document_to_cloudinary(document_file, user_id, document_title):
    """
    Upload document to Cloudinary for cloud storage.
    
    Args:
        document_file: File object to upload
        user_id (int): ID of uploading user
        document_title (str): Title for organization
        
    Returns:
        dict: Upload result with URL and metadata, or None if error
    """
    try:
        # Generate descriptive public ID
        safe_title = "".join(c for c in document_title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        public_id = f"user_{user_id}_{safe_title}_{int(time.time())}"
        
        # Upload document with metadata
        upload_result = cloudinary.uploader.upload(
            document_file,
            folder=Config.CLOUDINARY_FOLDER_DOCUMENTS,
            public_id=public_id,
            resource_type="auto",  # Auto-detect file type
            tags=['document', 'user_content'],
            context={
                'uploaded_by': f'user_{user_id}',
                'title': document_title
            }
        )
        
        return {
            'url': upload_result['secure_url'],
            'public_id': upload_result['public_id'],
            'format': upload_result['format'],
            'bytes': upload_result['bytes']
        }
        
    except Exception as e:
        print(f"❌ Error uploading document to Cloudinary: {e}")
        return None

# =============================================================================
# ENHANCED USER MODEL WITH CLOUDINARY
# =============================================================================

"""
Enhanced User model for Cloudinary integration.
Add this to your app/models.py file:

class User(UserMixin, db.Model):
    # ...existing fields...
    
    # Replace profile_image_filename with URL storage
    profile_image_url = db.Column(db.String(500))  # Store full Cloudinary URL
    cloudinary_public_id = db.Column(db.String(200))  # For image management
    
    @property
    def avatar_url(self):
        \"\"\"
        Get user's profile image URL with fallback to default.
        
        Returns:
            str: URL to user's profile image or default avatar
        \"\"\"
        if self.profile_image_url:
            return self.profile_image_url
        return url_for('static', filename='profile_pics/default_avatar.jpg')
    
    def update_profile_image(self, image_file):
        \"\"\"
        Update user's profile image using Cloudinary.
        
        Args:
            image_file: Uploaded image file
            
        Returns:
            bool: True if successful, False otherwise
        \"\"\"
        # Delete old image if exists
        if self.cloudinary_public_id:
            try:
                cloudinary.uploader.destroy(self.cloudinary_public_id)
            except:
                pass  # Continue even if deletion fails
        
        # Upload new image
        new_url = upload_profile_image_to_cloudinary(image_file, self.id)
        if new_url:
            self.profile_image_url = new_url
            # Extract public_id from URL for future management
            # This is a simplified extraction - implement based on your needs
            return True
        return False
"""

# =============================================================================
# INTEGRATION INSTRUCTIONS
# =============================================================================

"""
STEP-BY-STEP INTEGRATION GUIDE:

1. INSTALL CLOUDINARY:
   pip install cloudinary

2. ENVIRONMENT VARIABLES:
   export CLOUDINARY_CLOUD_NAME="your_cloud_name"
   export CLOUDINARY_API_KEY="your_api_key"
   export CLOUDINARY_API_SECRET="your_api_secret"
   export USE_CLOUDINARY="true"

3. UPDATE config.py:
   Add the Cloudinary configuration from above

4. UPDATE app/__init__.py:
   Add configure_cloudinary() call in create_app()

5. UPDATE models.py:
   Replace profile_image_filename with profile_image_url

6. UPDATE auth/routes.py:
   Replace local file upload with Cloudinary upload

7. UPDATE TEMPLATES:
   Update image URLs to use avatar_url property

MIGRATION CONSIDERATIONS:
- Backup existing profile images before migration
- Consider migrating existing images to Cloudinary
- Update database schema to use URLs instead of filenames
- Test thoroughly before production deployment

MONITORING AND MAINTENANCE:
- Monitor Cloudinary usage and costs
- Set up automatic cleanup for unused images
- Implement proper error handling and fallbacks
- Regular backup verification
"""
