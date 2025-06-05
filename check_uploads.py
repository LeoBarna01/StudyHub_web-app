"""
StudyHub Upload Validation Utility

This utility script validates the integrity of uploaded files in the StudyHub
application by checking for orphaned database records that reference missing files.

Purpose:
    - Scan all Document records in the database
    - Verify that corresponding files exist in the upload directory
    - Remove orphaned database records for missing files
    - Provide detailed reporting of cleanup operations

Usage:
    python check_uploads.py

Features:
    - Comprehensive file validation
    - Automatic cleanup of orphaned records
    - Detailed logging and reporting
    - Safe database transaction handling

Security Considerations:
    - Only removes database records, never deletes actual files
    - Uses database transactions for safe operations
    - Provides detailed audit trail of all changes

Author: StudyHub Development Team
License: MIT
"""

# =============================================================================
# CORE IMPORTS
# =============================================================================

import os  # Operating system interface for file operations
from app import create_app, db  # Flask application factory and database
from app.models import Document  # Document model for database operations

# =============================================================================
# UPLOAD VALIDATION LOGIC
# =============================================================================

def validate_uploads():
    """
    Validate integrity of uploaded files and clean orphaned database records.
    
    This function performs a comprehensive check of all documents in the database,
    verifying that their corresponding files exist in the upload directory.
    Any orphaned records (database entries without files) are safely removed.
    
    Process:
        1. Create Flask application context
        2. Retrieve upload folder configuration
        3. Query all documents from database
        4. Check file existence for each document
        5. Remove orphaned database records
        6. Provide detailed reporting
    
    Returns:
        None (prints results to console)
        
    Database Changes:
        - Removes Document records where files no longer exist
        - Commits changes using database transactions
        
    Error Handling:
        - Uses Flask application context for safe database access
        - Database transactions ensure data integrity
        - Detailed error reporting for troubleshooting
    """
    
    # Create Flask application instance with proper context
    app = create_app()

    with app.app_context():
        # Get configured upload directory path
        upload_folder = app.config['UPLOAD_FOLDER']
        print(f"🔍 Checking files in upload directory: {upload_folder}")
        print("=" * 60)
        
        # Initialize tracking variables
        missing_files = []
        
        # Query all documents from database
        all_docs = Document.query.all()
        print(f"📊 Total documents in database: {len(all_docs)}")
        
        # Validate each document's file existence
        for doc in all_docs:
            file_path = os.path.join(upload_folder, doc.filename)
            
            if not os.path.isfile(file_path):
                # File is missing - record for removal
                missing_files.append((doc.id, doc.title, doc.filename))
                print(f"❌ [MISSING] ID: {doc.id} | Title: {doc.title} | File: {doc.filename}")
                
                # Remove orphaned database record
                db.session.delete(doc)
            else:
                print(f"✅ [EXISTS] ID: {doc.id} | Title: {doc.title} | File: {doc.filename}")
        
        # Commit all database changes
        db.session.commit()
        
        # Generate final report
        print("=" * 60)
        print(f"📈 VALIDATION SUMMARY:")
        print(f"   • Total documents checked: {len(all_docs)}")
        print(f"   • Files found: {len(all_docs) - len(missing_files)}")
        print(f"   • Missing files (removed): {len(missing_files)}")
        
        if missing_files:
            print(f"\n🗑️  REMOVED ORPHANED RECORDS:")
            for doc_id, title, filename in missing_files:
                print(f"   • ID: {doc_id} | Title: {title} | File: {filename}")
        else:
            print(f"\n✅ All files are present and accounted for!")

# =============================================================================
# SCRIPT EXECUTION
# =============================================================================

if __name__ == '__main__':
    validate_uploads()
    
