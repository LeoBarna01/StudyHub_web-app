from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

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

    # One-to-many: documents uploaded by this user
    documents = db.relationship('Document', backref='author', lazy='dynamic')

    # Many-to-many: documents this user has favorited
    favorites = db.relationship(
        'Document',
        secondary=user_favorites,
        backref=db.backref('favorited_by', lazy='dynamic'),
        lazy='dynamic'
    )

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

class Question(db.Model):
    """Public support request submitted via the contact form."""
    id      = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100), nullable=False)
    email   = db.Column(db.String(120), nullable=False)
    body    = db.Column(db.Text, nullable=False)
    date    = db.Column(db.DateTime, server_default=db.func.now())