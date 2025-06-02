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
from app.upload.forms import UploadDocumentForm

@bp.route('/', methods=['GET', 'POST'])
@login_required
def upload_document():
    """
    Handle GET and POST requests for document uploads.

    GET:  Render the upload form with instructions.
    POST: Validate and save the uploaded file, then create a Document record.
    """
    form = UploadDocumentForm()
    if form.validate_on_submit():
        # Extract form fields from form object
        title = form.title.data
        description = form.description.data
        institute = form.institute.data
        course = form.course.data
        subject = form.subject.data
        category_name = form.category.data
        tags_string = form.tags.data
        file = form.file.data

        # Validate the uploaded file (still need allowed_file utility)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
            # Ensure the upload folder exists
            os.makedirs(os.path.join(current_app.root_path, upload_folder), exist_ok=True)
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
                author=current_user,
                # category and tags handled below
            )

            # Handle optional category
            if category_name:
                category = Category.query.filter_by(name=category_name).first()
                if not category:
                    category = Category(name=category_name)
                    db.session.add(category)
                doc.category = category

            # Handle tags (comma-separated)
            if tags_string:
                for tag_name in tags_string.split(','):
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
            # Redirect after successful upload
            return redirect(url_for('upload.upload_document')) # or redirect to profile/view page
        else:
            # Flash message for invalid file type is already in the template logic
            flash('Invalid file format. Allowed: PDF, DOC, DOCX, PPT, PPTX.', 'danger')

    # Render the upload page on GET or after form validation failure
    return render_template('upload/upload.html', form=form)