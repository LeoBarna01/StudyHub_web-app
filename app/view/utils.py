"""
app/view/utils.py - Document Viewing Utility Functions

This module provides utility functions for document browsing and filtering.
It includes functions for applying dynamic filters, retrieving popular
and recent documents, and other helper functions for the view module.

Functions:
- apply_filters: Dynamic query filtering for documents
- get_recent_documents: Retrieve recently uploaded documents
- get_popular_documents: Retrieve most downloaded documents

These utilities help organize and retrieve documents based on various criteria.
"""

# Import database models
from app.models import Document, User

# ============================================================================
# DOCUMENT FILTERING FUNCTIONS
# ============================================================================

def apply_filters(query, filters):
    """
    Apply dynamic filters to a Document query based on provided criteria.
    
    This function enables flexible document filtering based on various
    attributes including title, academic information, and author details.
    It supports partial matching for text fields and exact matching for
    structured data.
    
    Supported Filters:
    - title: Partial text match (case-insensitive)
    - institute: Exact match for academic institute
    - course: Exact match for course name
    - subject: Exact match for subject area
    - author: Partial match in author's first name (case-insensitive)
    - min_rating: Minimum rating threshold (if rating system exists)
    
    Args:
        query: SQLAlchemy query object for Document model
        filters (dict): Dictionary containing filter criteria
                       Keys correspond to filter types, values are filter values
                       
    Returns:
        SQLAlchemy query object: Modified query with applied filters
        
    Example:
        >>> filters = {'title': 'python', 'institute': 'MIT', 'author': 'john'}
        >>> filtered_query = apply_filters(Document.query, filters)
        >>> results = filtered_query.all()
    """
    # Apply title filter with partial, case-insensitive matching
    if filters.get('title'):
        query = query.filter(Document.title.ilike(f"%{filters['title']}%"))
    
    # Apply institute filter with exact matching
    if filters.get('institute'):
        query = query.filter_by(institute=filters['institute'])
    
    # Apply course filter with exact matching
    if filters.get('course'):
        query = query.filter_by(course=filters['course'])
    
    # Apply subject filter with exact matching
    if filters.get('subject'):
        query = query.filter_by(subject=filters['subject'])
    
    # Apply author filter with partial name matching
    # Requires JOIN with User table to access author information
    if filters.get('author'):
        query = query.join(User).filter(
            User.first_name.ilike(f"%{filters['author']}%")
        )
    
    # Note: min_rating filter implementation would go here if rating system exists
    # if filters.get('min_rating'):
    #     query = query.filter(Document.rating >= filters['min_rating'])
    
    return query

# ============================================================================
# DOCUMENT RETRIEVAL FUNCTIONS
# ============================================================================

def get_recent_documents(limit=5):
    """
    Retrieve the most recently uploaded documents.
    
    This function returns documents ordered by upload date in descending
    order (newest first). Useful for displaying recent activity and
    helping users discover new content.
    
    Args:
        limit (int): Maximum number of documents to return (default: 5)
        
    Returns:
        list: List of Document objects ordered by upload date (newest first)
        
    Example:
        >>> recent_docs = get_recent_documents(10)
        >>> print(f"Found {len(recent_docs)} recent documents")
    """
    return Document.query.order_by(Document.upload_date.desc()).limit(limit).all()


def get_popular_documents(limit=5):
    """
    Retrieve the most popular documents by download count.
    
    This function returns documents ordered by download count in descending
    order (most downloaded first). Helps users discover highly valued
    content and trending documents.
    
    Args:
        limit (int): Maximum number of documents to return (default: 5)
        
    Returns:
        list: List of Document objects ordered by download count (highest first)
        
    Example:
        >>> popular_docs = get_popular_documents(10)
        >>> for doc in popular_docs:
        ...     print(f"{doc.title}: {doc.downloads} downloads")
    """
    return Document.query.order_by(Document.downloads.desc()).limit(limit).all()