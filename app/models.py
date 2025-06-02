from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# -----------------------------------------------------------------------------
# Association Tables
# -----------------------------------------------------------------------------

# many-to-many: Document ↔ Tag
tags = db.Table(
    'tags',
    db.Column('document_id', db.Integer, db.ForeignKey('document.id'), primary_key=True),
    db.Column('tag_id',      db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)

# many-to-many: User ↔ Document favorites
user_favorites = db.Table(
    'user_favorites',
    db.Column('user_id',     db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('document_id', db.Integer, db.ForeignKey('document.id'), primary_key=True)
)

# many-to-many: User ↔ Document downloads
user_downloads = db.Table(
    'user_downloads',
    db.Column('user_id',     db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('document_id', db.Integer, db.ForeignKey('document.id'), primary_key=True)
)

# many-to-many: User ↔ Group members
group_members = db.Table(
    'group_members',
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

# -----------------------------------------------------------------------------
# Models
# -----------------------------------------------------------------------------

class User(UserMixin, db.Model):
    """
    Registered user with authentication and relationships.
    """
    id            = db.Column(db.Integer, primary_key=True)
    first_name    = db.Column(db.String(50), nullable=False)
    last_name     = db.Column(db.String(50), nullable=False)
    email         = db.Column(db.String(120), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    profile_image = db.Column(db.String(200), nullable=True, default='default_avatar.jpg')

    # One-to-many: documents uploaded by this user
    documents = db.relationship('Document', backref='author', lazy='dynamic')

    # Many-to-many: documents this user has favorited
    favorites = db.relationship(
        'Document',
        secondary=user_favorites,
        backref=db.backref('favorited_by', lazy='dynamic'),
        lazy='dynamic'
    )

    # Many-to-many: documents this user has downloaded
    downloads = db.relationship(
        'Document',
        secondary=user_downloads,
        backref=db.backref('downloaded_by', lazy='dynamic'),
        lazy='dynamic'
    )

    # One-to-many: questions submitted by this user
    questions = db.relationship('Question', backref='author', lazy='dynamic')

    # Many-to-many: groups this user is a member of - Defined using secondary table
    groups = db.relationship('Group', secondary='group_members', backref='members', lazy='dynamic')

    def set_password(self, password):
        """Hash and store the user's password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Return True if the given password matches the stored hash."""
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(user_id):
    """Flask-Login user loader callback."""
    return User.query.get(int(user_id))

class Category(db.Model):
    """Document category (e.g. Math, Physics)."""
    id        = db.Column(db.Integer, primary_key=True)
    name      = db.Column(db.String(100), unique=True, nullable=False)
    documents = db.relationship('Document', backref='category', lazy='dynamic')

class Tag(db.Model):
    """Free-form label for documents."""
    id        = db.Column(db.Integer, primary_key=True)
    name      = db.Column(db.String(100), unique=True, nullable=False)
    documents = db.relationship(
        'Document', secondary=tags,
        backref=db.backref('tags', lazy='dynamic')
    )

class Document(db.Model):
    """Uploaded study note with metadata and download tracking."""
    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    institute   = db.Column(db.String(200))
    course      = db.Column(db.String(200))
    subject     = db.Column(db.String(200))
    filename    = db.Column(db.String(200), nullable=False)
    upload_date = db.Column(db.DateTime, server_default=db.func.now())
    downloads   = db.Column(db.Integer, default=0)
    user_id     = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    rating      = db.Column(db.Float, default=0.0)

class Question(db.Model):
    """Public support request submitted via the contact form."""
    id      = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100), nullable=False)
    email   = db.Column(db.String(120), nullable=False)
    body    = db.Column(db.Text, nullable=False)
    date    = db.Column(db.DateTime, server_default=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# Forum Models
class Group(db.Model):
    """Study group for forum discussions."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    is_private = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    group_code = db.Column(db.String(5), unique=True, nullable=False)
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Relationships
    created_by = db.relationship('User', backref='created_groups', foreign_keys=[created_by_id])
    posts = db.relationship('GroupPost', back_populates='group', cascade='all, delete-orphan')

class GroupPost(db.Model):
    """Post in a group discussion."""
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    filename = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    # Relationships
    group = db.relationship('Group', back_populates='posts')
    author = db.relationship('User', backref='group_posts')
    
    # One-to-many: replies to this post
    replies = db.relationship('GroupReply', backref='post', lazy='dynamic', cascade='all, delete-orphan')

class GroupReply(db.Model):
    """Reply to a post in a group discussion."""
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('group_post.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    # Relationships
    author = db.relationship('User', backref='group_replies')

class GroupJoinRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), default='pending') # pending, accepted, rejected
    requested_at = db.Column(db.DateTime, default=datetime.utcnow)

    group = db.relationship('Group', backref='join_requests')
    user = db.relationship('User', backref='group_join_requests')

    __table_args__ = (db.UniqueConstraint('group_id', 'user_id', name='_user_group_uc'),)

    def __repr__(self):
        return f'<GroupJoinRequest {self.user.username} requests to join {self.group.name}>'

class Notification(db.Model):
    """
    User notifications for various events.
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False) # e.g., 'new_reply', 'group_invitation'
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)
    related_resource_id = db.Column(db.Integer, nullable=True)
    related_resource_type = db.Column(db.String(50), nullable=True)

    user = db.relationship('User', backref='notifications')

    def __repr__(self):
        return f'<Notification {self.type} for User {self.user_id}>'