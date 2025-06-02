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
    subject = StringField('Reference Subject', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    body = TextAreaField('Your Question', validators=[DataRequired(), Length(max=2000)])
    submit = SubmitField('Send Request')