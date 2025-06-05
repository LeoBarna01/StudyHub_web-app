"""
StudyHub Database Content Inspector

This utility script provides a quick overview of the database content
for the StudyHub application. It displays current data in key tables
to help with debugging, testing, and administrative tasks.

Purpose:
    - Quick database content inspection
    - Development and testing aid
    - Administrative overview
    - Data verification utility

Usage:
    python app/check_db_content.py

Features:
    - Displays all categories in the system
    - Shows available tags
    - Lists registered users (emails only for privacy)
    - Safe read-only operations
    - Clean formatted output

Security Considerations:
    - Only displays non-sensitive information
    - Uses read-only database queries
    - Protects user privacy (emails only, no passwords)
    - Safe for development and testing environments

Author: StudyHub Development Team
License: MIT
"""

# =============================================================================
# SYSTEM PATH CONFIGURATION
# =============================================================================

import sys
import os

# Add parent directory to Python path for proper module imports
# This allows the script to be run from any directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# =============================================================================
# APPLICATION IMPORTS
# =============================================================================

from app import create_app  # Flask application factory
from app.models import Category, User, Tag, Document  # Database models

# =============================================================================
# DATABASE INSPECTION FUNCTIONS
# =============================================================================

def inspect_database_content():
    """
    Inspect and display current database content.
    
    This function provides a comprehensive overview of the key data
    stored in the StudyHub database, organized by table and with
    clean formatting for easy reading.
    
    Tables Inspected:
        - Categories: Academic subject categories
        - Tags: Document classification tags  
        - Users: Registered user accounts (emails only)
        - Documents: Uploaded document summary
    
    Privacy Protection:
        - Only displays non-sensitive user information
        - Passwords and personal details are never shown
        - Email addresses shown for administrative purposes only
    """
    
    # Create Flask application context for database access
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("🔍 STUDYHUB DATABASE CONTENT INSPECTOR")
        print("=" * 60)
        
        # =============================================================================
        # CATEGORIES INSPECTION
        # =============================================================================
        
        categories = Category.query.all()
        print(f"\n📚 CATEGORIES ({len(categories)} total):")
        print("-" * 30)
        
        if categories:
            for idx, category in enumerate(categories, 1):
                print(f"  {idx}. {category.name}")
                if hasattr(category, 'description') and category.description:
                    print(f"     Description: {category.description}")
        else:
            print("  No categories found in database.")
        
        # =============================================================================
        # TAGS INSPECTION
        # =============================================================================
        
        tags = Tag.query.all()
        print(f"\n🏷️  TAGS ({len(tags)} total):")
        print("-" * 30)
        
        if tags:
            for idx, tag in enumerate(tags, 1):
                print(f"  {idx}. {tag.name}")
        else:
            print("  No tags found in database.")
        
        # =============================================================================
        # USERS INSPECTION
        # =============================================================================
        
        users = User.query.all()
        print(f"\n👥 USERS ({len(users)} total):")
        print("-" * 30)
        
        if users:
            for idx, user in enumerate(users, 1):
                full_name = f"{user.first_name} {user.last_name}" if hasattr(user, 'first_name') else "Unknown"
                print(f"  {idx}. {user.email} ({full_name})")
        else:
            print("  No users found in database.")
        
        # =============================================================================
        # DOCUMENTS INSPECTION
        # =============================================================================
        
        documents = Document.query.all()
        print(f"\n📄 DOCUMENTS ({len(documents)} total):")
        print("-" * 30)
        
        if documents:
            for idx, doc in enumerate(documents, 1):
                print(f"  {idx}. {doc.title}")
                if hasattr(doc, 'category') and doc.category:
                    print(f"     Category: {doc.category.name}")
                if hasattr(doc, 'filename'):
                    print(f"     File: {doc.filename}")
        else:
            print("  No documents found in database.")
        
        # =============================================================================
        # SUMMARY STATISTICS
        # =============================================================================
        
        print("\n" + "=" * 60)
        print("📊 DATABASE SUMMARY:")
        print(f"   • Categories: {len(categories)}")
        print(f"   • Tags: {len(tags)}")
        print(f"   • Users: {len(users)}")
        print(f"   • Documents: {len(documents)}")
        print("=" * 60)

# =============================================================================
# SCRIPT EXECUTION
# =============================================================================

if __name__ == "__main__":
    inspect_database_content()
