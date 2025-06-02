from flask import render_template, request, send_from_directory, current_app, jsonify
from flask_login import login_required, current_user
from app.view import bp
from app.models import Document, Category
from app.view.utils import apply_filters, get_recent_documents, get_popular_documents
from app import db

@bp.route('/', methods=['GET'])
def search():
    """
    Display search page and handle filtering of documents.
    GET parameters:
      - institute, course, subject, author, min_rating, category
    Also fetch recent and popular sections.
    """
    # Load all categories for the dropdown filter
    categories = Category.query.order_by(Category.name).all()

    # Collect filters from query string, including category
    filters = {
        'title':      request.args.get('title'),
        'institute':  request.args.get('institute'),
        'course':     request.args.get('course'),
        'subject':    request.args.get('subject'),
        'author':     request.args.get('author'),
        'min_rating': request.args.get('min_rating', type=float),
        'category':   request.args.get('category', type=int)
    }

    # Apply dynamic filters to the Document query
    docs_query = apply_filters(Document.query, filters)
    results   = docs_query.all()

    # Sections for recent and popular documents
    recent_docs  = get_recent_documents()
    # Load user's favorites
    user_favorites_docs = current_user.favorites.all() if current_user.is_authenticated else []

    # --- Debugging line ---
    print(f"DEBUG: User {current_user.id if current_user.is_authenticated else 'not authenticated'} favorites: {[doc.id for doc in user_favorites_docs]}")
    # --------------------

    return render_template(
        'view/search.html',
        documents=results,
        recent_documents=recent_docs,
        user_favorites_docs=user_favorites_docs,
        filters=filters,
        categories=categories
    )

@bp.route('/download/<int:doc_id>')
@login_required
def download(doc_id):
    """
    Serve a file download:
    - Fetch the Document or return 404
    - Increment its download counter
    - Send the file from UPLOAD_FOLDER as an attachment
    """
    doc = Document.query.get_or_404(doc_id)
    doc.downloads += 1
    db.session.commit()

    return send_from_directory(
        current_app.config['UPLOAD_FOLDER'],
        doc.filename,
        as_attachment=True
    )

@bp.route('/preview/<int:doc_id>')
@login_required
def preview(doc_id):
    """
    Serve a file for preview (e.g., in an iframe).
    - Fetch the Document or return 404
    - Serve the file from UPLOAD_FOLDER
    Note: Security consideration - ensure files are not malicious and handle sensitive data appropriately.
    """
    doc = Document.query.get_or_404(doc_id)

    # For preview, we don't want to force download, so serve inline
    return send_from_directory(
        current_app.config['UPLOAD_FOLDER'],
        doc.filename,
        as_attachment=False # Serve inline for preview
    )

@bp.route('/toggle_favorite/<int:doc_id>', methods=['POST'])
@login_required
def toggle_favorite(doc_id):
    """Toggle favorite status for a document."""
    document = Document.query.get_or_404(doc_id)
    
    if document in current_user.favorites:
        current_user.favorites.remove(document)
        is_favorited = False
        message = "Document removed from favorites"
    else:
        current_user.favorites.append(document)
        is_favorited = True
        message = "Document added to favorites"
    
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'is_favorited': is_favorited,
        'message': message
    })

@bp.route('/favorites')
@login_required
def favorites():
    """
    Display the current user's favorited documents.
    """
    user_favorites_docs = current_user.favorites.all()
    return render_template('view/favorites.html', favorites=user_favorites_docs)