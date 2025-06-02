from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from flask_wtf.file import FileField, FileAllowed
from app.models import User

class LoginForm(FlaskForm):
    """
    Form for user login.
    Fields:
      - email: user's email address
      - password: user's password
      - remember: optional 'remember me' checkbox
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    """
    Form for new user registration.
    Fields:
      - first_name: user's first name
      - last_name: user's last name
      - email: user's email address
      - password: user's password
      - confirm: password confirmation
    """
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=6),
            EqualTo('confirm', message='Passwords must match')
        ]
    )
    confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')

class EditProfileForm(FlaskForm):
    """
    Form for editing user profile details.
    Fields:
      - first_name: optional update
      - last_name: optional update
      - institute: user's institution
      - course: user's degree program
      - year: academic year
      - profile_image: user's profile picture
    """
    first_name = StringField('First Name', validators=[Length(max=50)])
    last_name = StringField('Last Name', validators=[Length(max=50)])
    institute = StringField('Institution', validators=[Length(max=100)])
    course = StringField('Degree Program', validators=[Length(max=100)])
    year = StringField('Academic Year', validators=[Length(max=10)])
    profile_image = FileField('Update Profile Picture', validators=[
        FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Images only!')
    ])
    submit = SubmitField('Save Changes')

class UpdateProfileForm(FlaskForm):
    """Form for updating user profile information."""
    profile_image = FileField('Profile Image', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')
    ])
    submit = SubmitField('Update Profile')