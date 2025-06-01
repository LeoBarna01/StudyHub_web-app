import os
from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash,
    current_app
)
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app import db
from . import bp
from app.upload.utils import allowed_file
from app.models import Document, Category, Tag

@bp.route('/', methods=['GET', 'POST'])
@login_required
def upload_document():
    """
    Handle GET and POST requests for document uploads.

    GET:  Render the upload form with instructions.
    POST: Validate and save the uploaded file, then create a Document record.
    """
    if request.method == 'POST':
        # Extract form fields
        title = request.form.get('title')
        description = request.form.get('description')
        institute = request.form.get('institute')
        course = request.form.get('course')
        subject = request.form.get('subject')
        # File upload
        file = request.files.get('file')

        # Validate the uploaded file
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
            file_path = os.path.join(current_app.root_path, upload_folder, filename)
            file.save(file_path)

            # Create Document model instance
            doc = Document(
                title=title,
                description=description,
                institute=institute,
                course=course,
                subject=subject,
                filename=filename,
                author=current_user
            )

            # Handle optional category
            category_name = request.form.get('category')
            if category_name:
                category = Category.query.filter_by(name=category_name).first()
                if not category:
                    category = Category(name=category_name)
                    db.session.add(category)
                doc.category = category

            # Handle tags (comma-separated)
            tags = request.form.get('tags')
            if tags:
                for tag_name in tags.split(','):
                    tag_name = tag_name.strip()
                    if not tag_name:
                        continue
                    tag = Tag.query.filter_by(name=tag_name).first()
                    if not tag:
                        tag = Tag(name=tag_name)
                        db.session.add(tag)
                    doc.tags.append(tag)

            # Save to database
            db.session.add(doc)
            db.session.commit()

            flash('Document uploaded successfully!', 'success')
            return redirect(url_for('upload.upload_document'))
        else:
            flash('Invalid file format. Allowed: PDF, DOC, DOCX, PPT, PPTX.', 'danger')

    # Render the upload page on GET or after failure
    return render_template('upload/upload.html')