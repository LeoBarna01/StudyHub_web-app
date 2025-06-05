"""
app/view/view.py - Document Viewing and Management Routes

This module handles all document viewing, browsing, and management functionality:
- Document search with advanced filtering
- Document downloads and previews
- Favorites management (add/remove favorites)
- User's uploaded documents display
- Document deletion by owners
- API endpoints for AJAX operations

Features:
- Advanced search and filtering capabilities
- Secure file serving for downloads and previews
- Real-time favorites management
- Document ownership validation
- Comprehensive error handling
"""

# Import Flask components
from flask import (
    render_template, request, send_from_directory, current_app,
    jsonify, abort, Response
)

# Import Flask-Login for authentication
from flask_login import login_required, current_user

# Import additional utilities
import os

# Import application components
from app.view import bp
from app.models import Document, Category
from app.view.utils import apply_filters, get_recent_documents, get_popular_documents
from app import db

# ============================================================================
# DOCUMENT SEARCH AND BROWSING ROUTES
# ============================================================================

@bp.route('/', methods=['GET'])
def search():
    """
    Display search page and handle document filtering with advanced options.
    
    This route serves as the main document discovery interface, providing:
    - Advanced filtering by multiple criteria
    - Category-based browsing
    - Recent documents showcase
    - User favorites integration
    - Dynamic search results
    
    URL Parameters (all optional):
        title: Partial text match in document title
        institute: Exact match for academic institute
        course: Exact match for course name
        subject: Exact match for subject area
        author: Partial match in author's first name
        min_rating: Minimum rating threshold (if implemented)
        category: Category ID for category-based filtering
    
    Features:
    - Dynamic query building based on provided filters
    - Category dropdown population from database
    - Recent documents section for discovery
    - User favorites integration for authenticated users
    - Debug logging for development
    
    Returns:
        Rendered search template with:
        - Filtered document results
        - Recent documents for discovery
        - User favorites (if authenticated)
        - Applied filters for form persistence
        - Available categories for filtering
    """
    # ========================================================================
    # LOAD CATEGORIES FOR FILTER DROPDOWN
    # ========================================================================
    
    # Load all categories ordered alphabetically for filter dropdown
    categories = Category.query.order_by(Category.name).all()

    # ========================================================================
    # COLLECT AND PROCESS FILTERS FROM QUERY PARAMETERS
    # ========================================================================
    
    # Extract filter parameters from URL query string
    filters = {
        'title':      request.args.get('title'),
        'institute':  request.args.get('institute'),
        'course':     request.args.get('course'),
        'subject':    request.args.get('subject'),
        'author':     request.args.get('author'),
        'min_rating': request.args.get('min_rating', type=float),
        'category':   request.args.get('category', type=int)
    }

    # ========================================================================
    # APPLY FILTERS AND RETRIEVE DOCUMENTS
    # ========================================================================
    
    # Start with base Document query
    docs_query = Document.query
    
    # Apply category filter if specified
    if filters.get('category'):
        docs_query = docs_query.filter_by(category_id=filters['category'])
    
    # Apply other dynamic filters using utility function
    docs_query = apply_filters(docs_query, filters)
    
    # Execute query to get filtered results
    results = docs_query.all()

    # ========================================================================
    # LOAD ADDITIONAL DATA FOR TEMPLATE
    # ========================================================================
    
    # Get recent documents for discovery section
    recent_docs = get_recent_documents()
    
    # Load user's favorites if authenticated
    user_favorites_docs = current_user.favorites.all() if current_user.is_authenticated else []

    # ========================================================================
    # DEBUG LOGGING (DEVELOPMENT)
    # ========================================================================
    
    # Debug information for development (remove in production)
    print(f"DEBUG: User {current_user.id if current_user.is_authenticated else 'not authenticated'} favorites: {[doc.id for doc in user_favorites_docs]}")

    # ========================================================================
    # RENDER TEMPLATE WITH ALL DATA
    # ========================================================================
    
    return render_template(
        'view/search.html',
        documents=results,              # Filtered search results
        recent_documents=recent_docs,   # Recent documents for discovery
        user_favorites_docs=user_favorites_docs,  # User's favorites
        filters=filters,                # Applied filters for form persistence
        categories=categories           # Available categories for dropdown
    )

# ============================================================================
# DOCUMENT DOWNLOAD AND PREVIEW ROUTES
# ============================================================================

@bp.route('/download/<int:doc_id>')
@login_required
def download(doc_id):
    """
    Serve document file for download with usage tracking.
    
    This route handles secure document downloads while tracking usage
    statistics. It validates document existence, increments download
    counters, and serves files with proper security measures.
    
    Features:
    - Document existence validation (404 if not found)
    - Download counter increment for analytics
    - Secure file serving from upload directory
    - Forced download (as_attachment=True)
    - Database transaction handling
    
    Args:
        doc_id (int): Unique identifier of the document to download
        
    Returns:
        File response: Document file served as attachment for download
        OR 404 error if document doesn't exist
        
    Security Notes:
    - Requires user authentication
    - Files served from configured UPLOAD_FOLDER only
    - No directory traversal vulnerabilities
    """
    # Validate document exists, return 404 if not found
    doc = Document.query.get_or_404(doc_id)
    
    # Increment download counter for analytics
    doc.downloads += 1
    
    # Save updated download count to database
    db.session.commit()

    # Serve file from configured upload folder as attachment (forces download)
    return send_from_directory(
        current_app.config['UPLOAD_FOLDER'],
        doc.filename,
        as_attachment=True  # Forces download instead of browser display
    )


@bp.route('/preview/<int:doc_id>')
@login_required
def preview(doc_id):
    """
    Serve document file for in-browser preview (e.g., in iframe).
    
    This route provides document preview functionality for supported
    file formats. It serves files inline for browser display rather
    than forcing downloads.
    
    Features:
    - Document existence validation with custom error page
    - Inline file serving for browser preview
    - Custom 404 response for missing documents
    - No download counter increment (preview only)
    
    Args:
        doc_id (int): Unique identifier of the document to preview
        
    Returns:
        File response: Document file served inline for preview
        OR Custom HTML 404 response for missing documents
        
    Security Considerations:
    - Requires user authentication
    - Files served from configured UPLOAD_FOLDER only
    - Consider file type validation for security
    - Be cautious with potentially malicious files
        
    Note:
        For production, consider additional security measures for
        file preview, especially for user-uploaded content.
    """
    # Check if document exists
    doc = Document.query.get(doc_id)
    
    if not doc:
        # Return custom minimal HTML page for not found
        # This provides better UX than standard 404 for iframe previews
        return Response(
            '''<html>
                <head>
                    <title>Document Not Found</title>
                </head>
                <body style="display:flex;align-items:center;justify-content:center;height:100vh;font-family:sans-serif;background:#fffbe6;">
                    <div style="text-align:center;">
                        <h2 style="color:#dc3545;">Document Not Found</h2>
                        <p>The document you are trying to preview does not exist or has been removed.</p>
                    </div>
                </body>
            </html>''',
            status=404,
            mimetype='text/html'
        )
    
    # Serve file inline for preview (not as attachment)
    return send_from_directory(
        current_app.config['UPLOAD_FOLDER'],
        doc.filename,
        as_attachment=False  # Serve inline for preview in browser
    )

# ============================================================================
# FAVORITES MANAGEMENT ROUTES
# ============================================================================

@bp.route('/toggle_favorite/<int:doc_id>', methods=['POST'])
@login_required
def toggle_favorite(doc_id):
    """
    Toggle favorite status for a document via AJAX.
    
    This route handles adding/removing documents from user favorites
    through AJAX requests. It provides real-time favorites management
    without page reloads.
    
    Features:
    - Document existence validation
    - Real-time favorites toggle functionality
    - Database transaction handling
    - JSON response for AJAX integration
    - User feedback messages
    
    Args:
        doc_id (int): Unique identifier of the document to toggle
        
    Returns:
        JSON response containing:
        - status: 'success' or 'error'
        - is_favorited: boolean indicating current favorite status
        - message: User-friendly status message
        
    HTTP Method: POST (for state-changing operation)
    Access Control: Requires user authentication
    """
    # Validate document exists, return 404 JSON if not found
    document = Document.query.get_or_404(doc_id)
    
    # Check current favorite status and toggle accordingly
    if document in current_user.favorites:
        # Document is currently favorited - remove it
        current_user.favorites.remove(document)
        is_favorited = False
        message = "Document removed from favorites"
    else:
        # Document is not favorited - add it
        current_user.favorites.append(document)
        is_favorited = True
        message = "Document added to favorites"
    
    # Save changes to database
    db.session.commit()
    
    # Return JSON response for AJAX handling
    return jsonify({
        'status': 'success',
        'is_favorited': is_favorited,
        'message': message
    })


@bp.route('/favorites')
@login_required
def favorites():
    """
    Display user's favorited documents page.
    
    This route shows all documents that the current user has marked
    as favorites, providing a personalized collection view.
    
    Features:
    - Load all user's favorited documents
    - Display in organized template
    - Quick access to favorite documents
    
    Returns:
        Rendered favorites template with user's favorite documents
        
    Access Control: Requires user authentication
    """
    # Load all documents favorited by current user
    user_favorites_docs = current_user.favorites.all()
    
    # Render favorites template with user's favorite documents
    return render_template('view/favorites.html', favorites=user_favorites_docs)

# ============================================================================
# API ENDPOINTS FOR AJAX OPERATIONS
# ============================================================================

@bp.route('/api/favorites')
@login_required
def api_favorites():
    """
    API endpoint returning user's favorite documents as JSON.
    
    This endpoint provides a JSON representation of the user's
    favorite documents, useful for AJAX requests, mobile apps,
    or other API consumers.
    
    Features:
    - Complete document information in JSON format
    - Author information included
    - Category information included
    - Download statistics included
    
    Returns:
        JSON array containing favorite documents with fields:
        - id: Document unique identifier
        - title: Document title
        - course: Academic course
        - institute: Academic institute
        - subject: Subject area
        - author: Author's full name
        - category: Category name (if assigned)
        - downloads: Download count
        
    Access Control: Requires user authentication
    Content-Type: application/json
    """
    # Load user's favorite documents
    user_favorites_docs = current_user.favorites.all()
    
    # Convert documents to JSON-serializable format
    favorites_data = [
        {
            'id': doc.id,
            'title': doc.title,
            'course': doc.course,
            'institute': doc.institute,
            'subject': doc.subject,
            'author': f"{doc.author.first_name} {doc.author.last_name}" if doc.author else "",
            'category': doc.category.name if doc.category else "",
            'downloads': doc.downloads
        }
        for doc in user_favorites_docs
    ]
    
    return jsonify(favorites_data)

# ============================================================================
# DOCUMENT MANAGEMENT ROUTES
# ============================================================================

@bp.route('/delete_document/<int:doc_id>', methods=['POST'])
@login_required
def delete_document(doc_id):
    """
    Delete a document (only by its owner) via AJAX.
    
    This route handles document deletion with proper authorization
    and file cleanup. Only the document owner can delete their uploads.
    
    Features:
    - Document existence validation
    - Owner authorization checking
    - Physical file deletion from filesystem
    - Database record cleanup
    - Transaction rollback on errors
    - JSON response for AJAX integration
    
    Args:
        doc_id (int): Unique identifier of the document to delete
        
    Returns:
        JSON response containing:
        - status: 'success' or 'error'
        - message: User-friendly status or error message
        
        HTTP status codes:
        - 200: Successful deletion
        - 403: Unauthorized (not document owner)
        - 404: Document not found
        - 500: Server error during deletion
        
    Security Features:
    - Owner-only authorization
    - Safe file deletion
    - Database transaction integrity
    
    HTTP Method: POST (for destructive operation)
    Access Control: Requires user authentication + document ownership
    """
    # Validate document exists, return 404 JSON if not found
    doc = Document.query.get_or_404(doc_id)
    
    # Check if current user is the document owner
    if doc.user_id != current_user.id:
        return jsonify({
            'status': 'error', 
            'message': 'You are not authorized to delete this document.'
        }), 403
    
    try:
        # ====================================================================
        # PHYSICAL FILE DELETION
        # ====================================================================
        
        # Construct full path to the document file
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], doc.filename)
        
        # Delete physical file if it exists
        if os.path.exists(file_path):
            os.remove(file_path)
        
        # ====================================================================
        # DATABASE RECORD DELETION
        # ====================================================================
        
        # Delete document record from database
        db.session.delete(doc)
        db.session.commit()
        
        return jsonify({
            'status': 'success', 
            'message': 'Document deleted successfully.'
        })
        
    except Exception as e:
        # Handle any errors during deletion process
        db.session.rollback()
        return jsonify({
            'status': 'error', 
            'message': f'An error occurred while deleting the document: {str(e)}'
        }), 500


@bp.route('/uploaded_documents')
@login_required
def uploaded_documents():
    """
    Display all documents uploaded by the current user.
    
    This route provides a personalized view of all documents that
    the current user has uploaded to the platform. It serves as
    a user's document management dashboard.
    
    Features:
    - Load all user's uploaded documents
    - Display in organized template
    - Provide document management interface
    - Quick access to user's contributions
    
    Returns:
        Rendered uploaded documents template with user's uploads
        
    Access Control: Requires user authentication
    
    Template Context:
        uploads: List of all documents uploaded by current user
    """
    # Load all documents uploaded by current user
    user_uploads = current_user.documents.all()
    
    # Render uploaded documents template
    return render_template('view/uploaded.html', uploads=user_uploads)