
"""
StudyHub Sample Data Population Utility

This utility script populates the StudyHub database with sample data
for development, testing, and demonstration purposes. It creates realistic
sample data that showcases the application's features.

Purpose:
    - Development environment setup
    - Testing data creation
    - Demonstration data for presentations
    - Quick application setup for new developers

Usage:
    python app/populate_sample_data.py

Data Created:
    - Academic categories (Mathematics, Physics, Computer Science, etc.)
    - Document classification tags (Notes, Exercises, Theory, etc.)
    - Sample user accounts with secure passwords
    - Realistic sample content for testing

Safety Features:
    - Checks for existing data to prevent duplicates
    - Uses secure password hashing
    - Transaction-safe database operations
    - Detailed logging of all operations

Author: StudyHub Development Team
License: MIT
"""

# =============================================================================
# SYSTEM PATH CONFIGURATION
# =============================================================================

import sys
import os

# Add parent directory to Python path for proper module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# =============================================================================
# APPLICATION IMPORTS
# =============================================================================

from app import db, create_app  # Database and application factory
from app.models import Category, User, Tag  # Database models

# =============================================================================
# SAMPLE DATA DEFINITIONS
# =============================================================================

# Academic categories with descriptions
SAMPLE_CATEGORIES = [
    {
        'name': 'Mathematics',
        'description': 'Mathematical subjects including calculus, algebra, statistics, and applied mathematics'
    },
    {
        'name': 'Physics',
        'description': 'Physics courses covering mechanics, thermodynamics, electromagnetism, and quantum physics'
    },
    {
        'name': 'Computer Science',
        'description': 'Programming, algorithms, data structures, software engineering, and computer systems'
    },
    {
        'name': 'Chemistry',
        'description': 'General chemistry, organic chemistry, physical chemistry, and laboratory work'
    },
    {
        'name': 'Biology',
        'description': 'Life sciences including molecular biology, genetics, ecology, and human anatomy'
    },
    {
        'name': 'Engineering',
        'description': 'Engineering disciplines including mechanical, electrical, civil, and software engineering'
    },
    {
        'name': 'Economics',
        'description': 'Economic theory, microeconomics, macroeconomics, and business studies'
    },
    {
        'name': 'Literature',
        'description': 'Literary studies, creative writing, linguistics, and language arts'
    }
]

# Document classification tags
SAMPLE_TAGS = [
    'Lecture Notes',
    'Exercise Solutions',
    'Theory Review',
    'Exam Preparation',
    'Study Guide',
    'Laboratory Report',
    'Project Documentation',
    'Reference Material',
    'Quick Reference',
    'Homework Solutions'
]

# Sample user accounts for testing
SAMPLE_USERS = [
    {
        'first_name': 'Alice',
        'last_name': 'Johnson',
        'email': 'alice.johnson@university.edu',
        'password': 'SecurePass123!'
    },
    {
        'first_name': 'Bob',
        'last_name': 'Smith',
        'email': 'bob.smith@university.edu',
        'password': 'StudentLife456!'
    },
    {
        'first_name': 'Carol',
        'last_name': 'Williams',
        'email': 'carol.williams@university.edu',
        'password': 'StudyHard789!'
    }
]

# =============================================================================
# DATA POPULATION FUNCTIONS
# =============================================================================

def populate_categories():
    """
    Create sample academic categories.
    
    Returns:
        int: Number of categories created
    """
    created_count = 0
    
    for cat_data in SAMPLE_CATEGORIES:
        # Check if category already exists
        existing = Category.query.filter_by(name=cat_data['name']).first()
        if not existing:
            category = Category(
                name=cat_data['name'],
                description=cat_data.get('description', '')
            )
            db.session.add(category)
            created_count += 1
            print(f"  ✅ Created category: {cat_data['name']}")
        else:
            print(f"  ⚠️  Category already exists: {cat_data['name']}")
    
    return created_count

def populate_tags():
    """
    Create sample document tags.
    
    Returns:
        int: Number of tags created
    """
    created_count = 0
    
    for tag_name in SAMPLE_TAGS:
        # Check if tag already exists
        existing = Tag.query.filter_by(name=tag_name).first()
        if not existing:
            tag = Tag(name=tag_name)
            db.session.add(tag)
            created_count += 1
            print(f"  ✅ Created tag: {tag_name}")
        else:
            print(f"  ⚠️  Tag already exists: {tag_name}")
    
    return created_count

def populate_users():
    """
    Create sample user accounts.
    
    Returns:
        int: Number of users created
    """
    created_count = 0
    
    for user_data in SAMPLE_USERS:
        # Check if user already exists
        existing = User.query.filter_by(email=user_data['email']).first()
        if not existing:
            user = User(
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                email=user_data['email']
            )
            # Set secure password using the model's hash method
            user.set_password(user_data['password'])
            db.session.add(user)
            created_count += 1
            print(f"  ✅ Created user: {user_data['email']}")
        else:
            print(f"  ⚠️  User already exists: {user_data['email']}")
    
    return created_count

# =============================================================================
# MAIN POPULATION FUNCTION
# =============================================================================

def populate_sample_data():
    """
    Populate the database with comprehensive sample data.
    
    This function creates all sample data in a transaction-safe manner,
    providing detailed logging and error handling.
    
    Process:
        1. Create Flask application context
        2. Populate categories with descriptions
        3. Create document classification tags
        4. Add sample user accounts
        5. Commit all changes to database
        6. Provide detailed summary report
    
    Returns:
        None (prints results to console)
        
    Error Handling:
        - Uses database transactions for safety
        - Checks for existing data to prevent duplicates
        - Provides detailed error reporting
        - Rolls back on any failures
    """
    
    print("=" * 60)
    print("🌱 STUDYHUB SAMPLE DATA POPULATION")
    print("=" * 60)
    
    try:
        # Create Flask application context
        app = create_app()
        
        with app.app_context():
            # Populate categories
            print("\n📚 Creating sample categories...")
            categories_created = populate_categories()
            
            # Populate tags
            print("\n🏷️  Creating sample tags...")
            tags_created = populate_tags()
            
            # Populate users
            print("\n👥 Creating sample users...")
            users_created = populate_users()
            
            # Commit all changes to database
            db.session.commit()
            
            # Generate summary report
            print("\n" + "=" * 60)
            print("✅ SAMPLE DATA POPULATION COMPLETED!")
            print("=" * 60)
            print(f"📊 SUMMARY:")
            print(f"   • Categories created: {categories_created}")
            print(f"   • Tags created: {tags_created}")
            print(f"   • Users created: {users_created}")
            print(f"   • Total items added: {categories_created + tags_created + users_created}")
            
            if users_created > 0:
                print(f"\n🔐 TEST LOGIN CREDENTIALS:")
                for user_data in SAMPLE_USERS:
                    print(f"   • {user_data['email']} : {user_data['password']}")
            
            print("=" * 60)
            
    except Exception as e:
        # Handle any errors gracefully
        print(f"\n❌ Error during data population: {e}")
        if 'db' in locals():
            db.session.rollback()
        print("Database changes have been rolled back.")

# =============================================================================
# SCRIPT EXECUTION
# =============================================================================

if __name__ == "__main__":
    populate_sample_data()
