from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileAllowed

class CreateGroupForm(FlaskForm):
    """Form for creating a new study group."""
    name = StringField('Group Name', validators=[
        DataRequired(),
        Length(min=3, max=100, message='Group name must be between 3 and 100 characters')
    ])
    description = TextAreaField('Description', validators=[
        DataRequired(),
        Length(max=1000, message='Description cannot exceed 1000 characters')
    ])
    is_private = BooleanField('Private Group')
    submit = SubmitField('Create Group')

class CreatePostForm(FlaskForm):
    """Form for creating a new post in a group."""
    title = StringField('Title', validators=[
        DataRequired(),
        Length(min=3, max=200, message='Title must be between 3 and 200 characters')
    ])
    content = TextAreaField('Content', validators=[
        DataRequired(),
        Length(max=5000, message='Content cannot exceed 5000 characters')
    ])
    file = FileField('Upload File', validators=[
        FileAllowed(['pdf', 'doc', 'docx', 'txt', 'zip', 'rar', 'jpg', 'jpeg', 'png'], 'Allowed file types: pdf, doc, docx, txt, zip, rar, jpg, jpeg, png')
    ])
    submit = SubmitField('Create Post')

class CreateReplyForm(FlaskForm):
    """Form for creating a new reply to a post."""
    content = TextAreaField('Reply', validators=[
        DataRequired(),
        Length(max=1000, message='Reply cannot exceed 1000 characters')
    ])
    submit = SubmitField('Post Reply') 