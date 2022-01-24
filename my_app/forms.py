from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, HiddenField, SelectField, EmailField
from wtforms.fields.simple import BooleanField
from wtforms.validators import DataRequired, Email, EqualTo,InputRequired, Length, ValidationError
from wtforms_validators import Alpha, AlphaNumeric
from my_app.models import User

class RegistrationForm(FlaskForm):
    first_name = StringField(label='first_name', validators=[InputRequired(message='First name is required'), Length(min=5,max=20), Alpha(message='First name can only contain letters')])
    email = EmailField(label='email', validators= [InputRequired('Email is required'), Email(message= 'Email is of invalid format')])
    username = StringField('username', validators= [InputRequired(message = 'Please select a username'), Length(min=5,max=20)])
    password = PasswordField(label='Password', validators=[InputRequired(message='Enter a password'),Length(min=5,max=20),EqualTo('confirm_password',message='Passwords must match')])
    confirm_password = PasswordField(label='Confirm_Password')
    submit = SubmitField(label='Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists, please select a different one')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken, please select a different one')

class LoginForm(FlaskForm):
    email = StringField('email', validators= [InputRequired(message='Email is required'), Length(min=5,max=50)])
    password = PasswordField('Password',validators=[InputRequired(message='Password cannot be blank'), Length(min=5,max=20)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class PostForm(FlaskForm):
    title = StringField('Title', validators = [DataRequired()])
    content = TextAreaField('Content', validators =[DataRequired()])
    submit = SubmitField('Post')


class CommentForm(FlaskForm):
    body = StringField('Body', validators=[InputRequired()])
    author = HiddenField('author')

class RatingForm(FlaskForm):
    rate = HiddenField('rate', validators=[InputRequired()])

class SortPostsForm(FlaskForm):
    sorted = SelectField('sort', choices = [('date_asc', 'Ascending'), ('date_desc', 'Descending')])