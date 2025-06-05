"""
StudyHub Database Models

This module defines the database structure using SQLAlchemy ORM for the StudyHub
web application. It contains all table models and their relationships to support
academic document sharing, user management, and platform functionality.

Database Schema Overview:
    - User: Registered platform users with authentication
    - Document: Academic documents uploaded by users
    - Category: Document categorization system
    - Tag: Flexible document labeling system
    - Question: Contact form submissions and support requests

Key Relationships:
    - One-to-Many: User → Documents (users can upload multiple documents)
    - Many-to-Many: User ↔ Documents (favorites and download tracking)
    - Many-to-Many: Document ↔ Tags (flexible document tagging)
    - One-to-Many: Category → Documents (document categorization)

Security Features:
    - Password hashing using Werkzeug
    - Flask-Login integration for session management
    - Foreign key constraints for data integrity

Author: StudyHub Development Team
License: MIT
"""

# =============================================================================
# IMPORTS AND DEPENDENCIES
# =============================================================================

# Core Flask and database imports
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask import url_for

# =============================================================================
# ASSOCIATION TABLES FOR MANY-TO-MANY RELATIONSHIPS
# =============================================================================

# Document-Tag association table
# Enables many-to-many relationship: documents can have multiple tags,
# and tags can be associated with multiple documents
document_tags = db.Table(
    'document_tags',
    db.Column('document_id', db.Integer, db.ForeignKey('document.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)

# User-Document favorites association table
# Tracks which documents users have marked as favorites
# Many-to-many: users can favorite multiple documents,
# documents can be favorited by multiple users
user_favorites = db.Table(
    'user_favorites',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('document_id', db.Integer, db.ForeignKey('document.id'), primary_key=True)
)

# User-Document downloads association table  
# Tracks download history for analytics and user activity
# Many-to-many: users can download multiple documents,
# documents can be downloaded by multiple users
user_downloads = db.Table(
    'user_downloads',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('document_id', db.Integer, db.ForeignKey('document.id'), primary_key=True)
)

# =============================================================================
# DATABASE MODELS
# =============================================================================

class User(UserMixin, db.Model):
    """
    User model for registered platform users.
    
    This model handles user authentication, profile management, and relationships
    with documents. It inherits from UserMixin to provide Flask-Login integration
    with automatic properties:
    - is_authenticated: True if user is logged in
    - is_active: True if user account is active  
    - is_anonymous: False for real users (True for anonymous)
    - get_id(): Returns user ID as string for session management
    
    Security Features:
    - Password hashing using Werkzeug
    - Email uniqueness enforcement
    - Safe profile image handling
    
    Relationships:
    - One-to-Many: User → Documents (uploaded documents)
    - Many-to-Many: User ↔ Documents (favorites and downloads)
    - One-to-Many: User → Questions (contact form submissions)
    """
    
    # =========================================================================
    # TABLE COLUMNS
    # =========================================================================
    
    # Primary key and basic identification
    id = db.Column(db.Integer, primary_key=True)
    
    # Personal information (required fields)
    first_name = db.Column(db.String(50), nullable=False, index=True)
    last_name = db.Column(db.String(50), nullable=False, index=True)
    
    # Authentication fields
    email = db.Column(db.String(120), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    
    # Profile customization
    profile_image = db.Column(
        db.String(200), 
        nullable=True, 
        default='default_avatar.jpg'
    )
    
    # Account metadata
    registration_date = db.Column(
        db.DateTime, 
        server_default=db.func.now(),
        nullable=False
    )
    
    # =========================================================================
    # COMPUTED PROPERTIES
    # =========================================================================
    
    @property
    def full_name(self):
        """
        Return user's full name by combining first and last name.
        
        Returns:
            str: Full name in format "First Last"
        """
        return f"{self.first_name} {self.last_name}"
    
    @property
    def avatar_url(self):
        """
        Generate URL for user's profile image.
        
        Handles both custom uploaded images and default avatar.
        Custom images are served from uploads directory, while
        default avatar is served from static assets.
        
        Returns:
            str: Complete URL to user's profile image
        """
        if self.profile_image and self.profile_image != 'default_avatar.jpg':
            # Custom uploaded profile image
            return url_for('auth.profile_pic', filename=self.profile_image)
        else:
            # Default avatar from static assets
            return url_for('static', filename='profile_pics/default_avatar.jpg')
    
    @property
    def document_count(self):
        """
        Get total number of documents uploaded by this user.
        
        Returns:
            int: Count of user's uploaded documents
        """
        return self.documents.count()
    
    @property
    def favorites_count(self):
        """
        Get total number of documents favorited by this user.
        
        Returns:
            int: Count of user's favorite documents
        """
        return self.favorites.count()
    
    # =========================================================================
    # RELATIONSHIPS WITH OTHER MODELS
    # =========================================================================
    
    # One-to-Many: User can upload multiple documents
    documents = db.relationship(
        'Document', 
        backref='author', 
        lazy='dynamic',
        cascade='all, delete-orphan'  # Delete documents when user is deleted
    )
    
    # Many-to-Many: User's favorite documents
    favorites = db.relationship(
        'Document',
        secondary=user_favorites,
        backref=db.backref('favorited_by', lazy='dynamic'),
        lazy='dynamic'
    )
    
    # Many-to-Many: User's download history
    downloads = db.relationship(
        'Document',
        secondary=user_downloads,
        backref=db.backref('downloaded_by', lazy='dynamic'),
        lazy='dynamic'
    )
    
    # One-to-Many: Contact form questions submitted by user
    questions = db.relationship(
        'Question', 
        backref='author', 
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    
    # =========================================================================
    # PASSWORD MANAGEMENT METHODS
    # =========================================================================
    
    def set_password(self, password):
        """
        Hash and store user password securely.
        
        Uses Werkzeug's password hashing for security. The plain text
        password is never stored in the database.
        
        Args:
            password (str): Plain text password to hash and store
        """
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """
        Verify if provided password matches stored hash.
        
        Args:
            password (str): Plain text password to verify
            
        Returns:
            bool: True if password is correct, False otherwise
        """
        return check_password_hash(self.password_hash, password)
    
    # =========================================================================
    # UTILITY METHODS
    # =========================================================================
    
    def is_favorite(self, document):
        """
        Check if a document is in user's favorites.
        
        Args:
            document (Document): Document to check
            
        Returns:
            bool: True if document is favorited, False otherwise
        """
        return self.favorites.filter_by(id=document.id).first() is not None
    
    def has_downloaded(self, document):
        """
        Check if user has downloaded a specific document.
        
        Args:
            document (Document): Document to check
            
        Returns:
            bool: True if user has downloaded document, False otherwise
        """
        return self.downloads.filter_by(id=document.id).first() is not None
    
    def __repr__(self):
        """String representation for debugging."""
        return f'<User {self.full_name} ({self.email})>'


# =============================================================================
# FLASK-LOGIN INTEGRATION
# =============================================================================

@login.user_loader
def load_user(user_id):
    """
    User loader callback for Flask-Login.
    
    This function is called by Flask-Login to load a user object from
    the database for each request. It's required for session management
    and user authentication.
    
    Args:
        user_id (str): User ID as string from session
        
    Returns:
        User: User object if found, None otherwise
    """
    return User.query.get(int(user_id))


# =============================================================================
# DOCUMENT CATEGORIZATION MODELS
# =============================================================================

class Category(db.Model):
    """
    Document category model for organizing academic content.
    
    Categories provide a structured way to classify documents by
    academic field (e.g., Mathematics, Physics, Computer Science).
    This helps users discover relevant content and enables
    targeted searching and filtering.
    
    Features:
    - Unique category names to prevent duplicates
    - One-to-many relationship with documents
    - Indexed name field for efficient searching
    """
    
    # =========================================================================
    # TABLE COLUMNS
    # =========================================================================
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(
        db.String(100), 
        unique=True, 
        nullable=False, 
        index=True
    )
    description = db.Column(db.Text, nullable=True)
    
    # Category metadata
    created_date = db.Column(
        db.DateTime, 
        server_default=db.func.now(),
        nullable=False
    )
    
    # =========================================================================
    # RELATIONSHIPS
    # =========================================================================
    
    # One-to-Many: Category can contain multiple documents
    documents = db.relationship(
        'Document', 
        backref='category', 
        lazy='dynamic'
    )
    
    # =========================================================================
    # UTILITY METHODS
    # =========================================================================
    
    @property
    def document_count(self):
        """
        Get total number of documents in this category.
        
        Returns:
            int: Count of documents in category
        """
        return self.documents.count()
    
    def __repr__(self):
        """String representation for debugging."""
        return f'<Category {self.name}>'


class Tag(db.Model):
    """
    Flexible tag model for document labeling.
    
    Tags provide a flexible, user-driven classification system
    that complements the structured category system. Users can
    create and apply multiple tags to documents for granular
    organization (e.g., "exam", "summary", "formulas").
    
    Features:
    - Many-to-many relationship with documents
    - Unique tag names to prevent duplicates
    - Case-insensitive searching support
    """
    
    # =========================================================================
    # TABLE COLUMNS
    # =========================================================================
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(
        db.String(50), 
        unique=True, 
        nullable=False, 
        index=True
    )
    
    # Tag metadata
    created_date = db.Column(
        db.DateTime, 
        server_default=db.func.now(),
        nullable=False
    )
    usage_count = db.Column(db.Integer, default=0)  # Track tag popularity
    
    # =========================================================================
    # RELATIONSHIPS
    # =========================================================================
    
    # Many-to-Many: Tags can be applied to multiple documents,
    # documents can have multiple tags
    documents = db.relationship(
        'Document', 
        secondary=document_tags,
        backref=db.backref('tags', lazy='dynamic'),
        lazy='dynamic'
    )
    
    # =========================================================================
    # UTILITY METHODS
    # =========================================================================
    
    @property
    def document_count(self):
        """
        Get total number of documents with this tag.
        
        Returns:
            int: Count of documents tagged with this tag
        """
        return self.documents.count()
    
    def increment_usage(self):
        """Increment usage counter when tag is applied to a document."""
        self.usage_count += 1
        db.session.commit()
    
    @classmethod
    def get_or_create(cls, tag_name):
        """
        Get existing tag or create new one if it doesn't exist.
        
        Args:
            tag_name (str): Name of the tag (case-insensitive)
            
        Returns:
            Tag: Existing or newly created tag
        """
        # Normalize tag name (lowercase, stripped)
        normalized_name = tag_name.strip().lower()
        
        # Try to find existing tag
        tag = cls.query.filter_by(name=normalized_name).first()
        
        if not tag:
            # Create new tag if it doesn't exist
            tag = cls(name=normalized_name)
            db.session.add(tag)
            db.session.commit()
        
        return tag
    
    def __repr__(self):
        """String representation for debugging."""
        return f'<Tag {self.name}>'


# =============================================================================
# CORE DOCUMENT MODEL
# =============================================================================

class Document(db.Model):
    """
    Academic document model for user-uploaded study materials.
    
    This is the core model representing academic documents (PDFs, images)
    uploaded by users. It stores both file metadata and academic context
    to enable effective search, categorization, and sharing.
    
    Features:
    - Complete academic metadata (course, institute, subject)
    - Download tracking and analytics
    - Rating system for quality assessment
    - Flexible categorization and tagging
    - User favorites and download history
    - File management and serving
    
    Security Considerations:
    - File validation handled at upload time
    - Safe filename storage prevents directory traversal
    - User ownership tracking for access control
    """
    
    # =========================================================================
    # CORE DOCUMENT INFORMATION
    # =========================================================================
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Document content metadata
    title = db.Column(db.String(200), nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    filename = db.Column(db.String(200), nullable=False)
    original_filename = db.Column(db.String(200), nullable=True)
    file_size = db.Column(db.Integer, nullable=True)  # Size in bytes
    file_type = db.Column(db.String(10), nullable=True)  # Extension (pdf, jpg, etc.)
    
    # =========================================================================
    # ACADEMIC METADATA
    # =========================================================================
    
    institute = db.Column(db.String(200), nullable=True, index=True)
    course = db.Column(db.String(200), nullable=True, index=True)
    subject = db.Column(db.String(200), nullable=True, index=True)
    academic_year = db.Column(db.String(20), nullable=True)  # e.g., "2024-2025"
    
    # =========================================================================
    # TRACKING AND ANALYTICS
    # =========================================================================
    
    upload_date = db.Column(
        db.DateTime, 
        server_default=db.func.now(),
        nullable=False,
        index=True
    )
    last_modified = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        onupdate=db.func.now()
    )
    
    # Usage statistics
    downloads = db.Column(db.Integer, default=0, nullable=False)
    views = db.Column(db.Integer, default=0, nullable=False)
    rating = db.Column(db.Float, default=0.0, nullable=False)
    rating_count = db.Column(db.Integer, default=0, nullable=False)
    
    # Content flags and moderation
    is_public = db.Column(db.Boolean, default=True, nullable=False)
    is_featured = db.Column(db.Boolean, default=False, nullable=False)
    
    # =========================================================================
    # FOREIGN KEY RELATIONSHIPS
    # =========================================================================
    
    # Owner of the document (required)
    user_id = db.Column(
        db.Integer, 
        db.ForeignKey('user.id'), 
        nullable=False,
        index=True
    )
    
    # Category classification (optional)
    category_id = db.Column(
        db.Integer, 
        db.ForeignKey('category.id'), 
        nullable=True,
        index=True
    )
    
    # =========================================================================
    # COMPUTED PROPERTIES
    # =========================================================================
    
    @property
    def author_name(self):
        """
        Get document author's full name.
        
        Returns:
            str: Author's full name or "Unknown" if author is deleted
        """
        return self.author.full_name if self.author else "Unknown Author"
    
    @property
    def file_size_human(self):
        """
        Get human-readable file size.
        
        Returns:
            str: File size in KB, MB, etc.
        """
        if not self.file_size:
            return "Unknown size"
        
        for unit in ['B', 'KB', 'MB', 'GB']:
            if self.file_size < 1024.0:
                return f"{self.file_size:.1f} {unit}"
            self.file_size /= 1024.0
        return f"{self.file_size:.1f} TB"
    
    @property
    def category_name(self):
        """
        Get category name or default if no category assigned.
        
        Returns:
            str: Category name or "Uncategorized"
        """
        return self.category.name if self.category else "Uncategorized"
    
    @property
    def tag_list(self):
        """
        Get list of tag names for this document.
        
        Returns:
            list: List of tag names
        """
        return [tag.name for tag in self.tags.all()]
    
    @property
    def average_rating(self):
        """
        Calculate average rating for display.
        
        Returns:
            float: Average rating (0.0 if no ratings)
        """
        if self.rating_count > 0:
            return round(self.rating / self.rating_count, 1)
        return 0.0
    
    @property
    def is_recently_uploaded(self):
        """
        Check if document was uploaded within last 7 days.
        
        Returns:
            bool: True if uploaded recently
        """
        from datetime import timedelta
        recent_threshold = datetime.utcnow() - timedelta(days=7)
        return self.upload_date > recent_threshold
    
    # =========================================================================
    # UTILITY METHODS
    # =========================================================================
    
    def increment_downloads(self):
        """Safely increment download counter."""
        self.downloads += 1
        db.session.commit()
    
    def increment_views(self):
        """Safely increment view counter."""
        self.views += 1
        db.session.commit()
    
    def add_rating(self, rating_value):
        """
        Add a new rating to the document.
        
        Args:
            rating_value (float): Rating value (1.0 to 5.0)
        """
        if 1.0 <= rating_value <= 5.0:
            self.rating += rating_value
            self.rating_count += 1
            db.session.commit()
    
    def add_tag(self, tag_name):
        """
        Add a tag to this document.
        
        Args:
            tag_name (str): Name of the tag to add
        """
        tag = Tag.get_or_create(tag_name)
        if tag not in self.tags.all():
            self.tags.append(tag)
            tag.increment_usage()
            db.session.commit()
    
    def remove_tag(self, tag_name):
        """
        Remove a tag from this document.
        
        Args:
            tag_name (str): Name of the tag to remove
        """
        tag = Tag.query.filter_by(name=tag_name.lower()).first()
        if tag and tag in self.tags.all():
            self.tags.remove(tag)
            db.session.commit()
    
    def is_owned_by(self, user):
        """
        Check if document is owned by specific user.
        
        Args:
            user (User): User to check ownership for
            
        Returns:
            bool: True if user owns this document
        """
        return self.user_id == user.id if user else False
    
    def __repr__(self):
        """String representation for debugging."""
        return f'<Document {self.title} by {self.author_name}>'


# =============================================================================
# SUPPORT AND COMMUNICATION MODELS  
# =============================================================================

class Question(db.Model):
    """
    Contact form submission model for user support requests.
    
    This model stores questions and support requests submitted through
    the contact form. It supports both authenticated and anonymous
    submissions for maximum accessibility.
    
    Features:
    - Anonymous and authenticated submissions
    - Email tracking for follow-up
    - Subject categorization
    - Response tracking and status management
    """
    
    # =========================================================================
    # TABLE COLUMNS
    # =========================================================================
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Message content
    subject = db.Column(db.String(200), nullable=False, index=True)
    email = db.Column(db.String(120), nullable=False, index=True)
    body = db.Column(db.Text, nullable=False)
    
    # Submission metadata
    submission_date = db.Column(
        db.DateTime, 
        server_default=db.func.now(),
        nullable=False,
        index=True
    )
    
    # Support management
    status = db.Column(
        db.String(20), 
        default='open', 
        nullable=False
    )  # open, in_progress, resolved, closed
    priority = db.Column(
        db.String(10), 
        default='normal', 
        nullable=False
    )  # low, normal, high, urgent
    
    # Response tracking
    response_sent = db.Column(db.Boolean, default=False, nullable=False)
    response_date = db.Column(db.DateTime, nullable=True)
    
    # =========================================================================
    # FOREIGN KEY RELATIONSHIPS
    # =========================================================================
    
    # Optional link to authenticated user (None for anonymous submissions)
    user_id = db.Column(
        db.Integer, 
        db.ForeignKey('user.id'), 
        nullable=True,
        index=True
    )
    
    # =========================================================================
    # UTILITY METHODS
    # =========================================================================
    
    @property
    def author_name(self):
        """
        Get question author's name.
        
        Returns:
            str: Author's full name or email if anonymous
        """
        if self.author:
            return self.author.full_name
        return f"Anonymous ({self.email})"
    
    @property
    def is_recent(self):
        """
        Check if question was submitted recently (within 24 hours).
        
        Returns:
            bool: True if submitted recently
        """
        from datetime import timedelta
        recent_threshold = datetime.utcnow() - timedelta(hours=24)
        return self.submission_date > recent_threshold
    
    @property
    def needs_response(self):
        """
        Check if question needs a response.
        
        Returns:
            bool: True if question is open and hasn't been responded to
        """
        return self.status == 'open' and not self.response_sent
    
    def mark_as_responded(self):
        """Mark question as responded to."""
        self.response_sent = True
        self.response_date = datetime.utcnow()
        if self.status == 'open':
            self.status = 'in_progress'
        db.session.commit()
    
    def close_question(self):
        """Mark question as resolved and closed."""
        self.status = 'resolved'
        db.session.commit()
    
    def __repr__(self):
        """String representation for debugging."""
        return f'<Question {self.subject} from {self.author_name}>'