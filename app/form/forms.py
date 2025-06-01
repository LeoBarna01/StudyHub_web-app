from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class QuestionForm(FlaskForm):
    """
    Public question/contact form.
    Fields:
      - subject: reference subject or topic
      - email: requester's email
      - body: detailed question or message
    """
    subject = SelectField(
        'Reference Subject',
        choices=[
            ('General', 'General'),
            ('Math', 'Math'),
            ('Physics', 'Physics'),
            ('Other', 'Other')
        ],
        validators=[DataRequired()]
    )
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    body = TextAreaField('Your Question', validators=[DataRequired(), Length(max=2000)])
    submit = SubmitField('Send Request')