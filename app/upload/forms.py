from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length

class UploadDocumentForm(FlaskForm):
    """
    Form for uploading a new document.
    """
    title = StringField('Document Title', validators=[DataRequired(), Length(max=200)])
    institute = StringField('Academic Institute', validators=[Length(max=200)])
    year = StringField('Academic Year', validators=[Length(max=50)]) # Changed from IntegerField to StringField for flexibility
    course = StringField('Academic Course', validators=[Length(max=200)])
    subject = StringField('Subject', validators=[Length(max=200)])
    # Author is the current logged-in user, not a form field
    description = TextAreaField('Brief description of the document')
    category = StringField('Category', validators=[Length(max=100)])
    tags = StringField('Tags (comma-separated)', validators=[Length(max=200)])
    file = FileField('Select Document', validators=[DataRequired()])
    submit = SubmitField('Upload Document') 