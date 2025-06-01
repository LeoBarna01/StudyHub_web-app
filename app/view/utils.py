from app.models import Document, User

def apply_filters(query, filters):
    """
    Apply dynamic filters to a Document query based on provided dict:
      filters may include 'institute', 'course', 'subject', 'author', 'min_rating'.
    Returns a filtered query.
    """
    if filters.get('institute'):
        query = query.filter_by(institute=filters['institute'])
    if filters.get('course'):
        query = query.filter_by(course=filters['course'])
    if filters.get('subject'):
        query = query.filter_by(subject=filters['subject'])
    if filters.get('author'):
        # join User to filter by author's name
        query = query.join(User).filter(
            User.first_name.ilike(f"%{filters['author']}%")
        )
    if filters.get('min_rating'):
        query = query.filter(Document.rating >= filters['min_rating'])
    return query

def get_recent_documents(limit=5):
    """
    Return the most recent documents, limited by the given number.
    """
    return Document.query.order_by(Document.upload_date.desc()).limit(limit).all()

def get_popular_documents(limit=5):
    """
    Return the most popular documents by download count.
    """
    return Document.query.order_by(Document.downloads.desc()).limit(limit).all()