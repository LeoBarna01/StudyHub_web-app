"""
StudyHub Database Initialization Script

This script initializes a fresh database for the StudyHub application.
It creates all necessary tables based on the current SQLAlchemy models
and optionally populates them with sample data.

Usage:
    python init_db.py

Features:
    - Creates all database tables from SQLAlchemy models
    - Handles database connection errors gracefully
    - Provides clear feedback on initialization status
    - Can be extended to include sample data population

Author: StudyHub Development Team
License: MIT
"""

# =============================================================================
# CORE IMPORTS
# =============================================================================

from app import create_app, db
from app.models import User, Category, Tag, Document, Question

# =============================================================================
# DATABASE INITIALIZATION
# =============================================================================

def init_db():
    """
    Initialize the StudyHub database with all required tables.
    
    This function creates a Flask application context and initializes
    all database tables based on the current SQLAlchemy model definitions.
    
    Steps performed:
        1. Create Flask application instance
        2. Establish application context
        3. Create all database tables
        4. Provide success confirmation
    
    Raises:
        Exception: If database creation fails due to permissions or configuration
    """
    try:
        # Create Flask application instance
        app = create_app()
        
        # Use application context for database operations
        with app.app_context():
            # Create all tables based on model definitions
            db.create_all()
            print("✅ Database tables created successfully!")
            print("📊 Tables created:")
            print("   - users (User accounts and authentication)")
            print("   - categories (Document categories)")
            print("   - tags (Document tags)")
            print("   - documents (Uploaded documents)")
            print("   - questions (Contact form submissions)")
            print("   - document_tags (Many-to-many relationship)")
            
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        print("🔧 Please check:")
        print("   - Database file permissions")
        print("   - Configuration in config.py")
        print("   - SQLAlchemy model definitions")
        raise

# =============================================================================
# SCRIPT EXECUTION
# =============================================================================

if __name__ == '__main__':
    print("🚀 Initializing StudyHub database...")
    init_db() 