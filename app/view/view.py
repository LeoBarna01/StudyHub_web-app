from flask import render_template, request, send_from_directory, current_app
from flask_login import login_required
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
    popular_docs = get_popular_documents()

    return render_template(
        'view/search.html',
        documents=results,
        recent_documents=recent_docs,
        popular_documents=popular_docs,
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