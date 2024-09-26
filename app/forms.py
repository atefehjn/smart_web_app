from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,BooleanField,validators
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
import re

def validate_password(form, field):
    password = field.data
    if not re.search(r'[A-Z]', password):
        raise ValidationError('Password must contain at least one uppercase letter.')
    if not re.search(r'[a-z]', password):
        raise ValidationError('Password must contain at least one lowercase letter.')
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise ValidationError('Password must contain at least one special character.')
    if not re.search(r'\d', password):
        raise ValidationError('Password must contain at least one digit.')

class RegistrationForm(FlaskForm):
    username = StringField('', 
                           validators=[DataRequired(), Length(min=3, message="Username must be at least 3 characters long.")])
    email = StringField('', 
                        validators=[DataRequired(), Email(message="Please enter a valid email address.")])
    password = PasswordField('', 
                             validators=[
                                 DataRequired(), 
                                 Length(min=8, message="Password must be at least 8 characters long."),
                                 validate_password
                             ])
    confirm_password = PasswordField('', 
                                     validators=[
                                         DataRequired(), 
                                         EqualTo('password', message="Passwords must match.")
                                     ])

    agree_tos = BooleanField('I agree to the Terms of Service', validators=[DataRequired()])
    submit = SubmitField('Sign Up')
    

class SignInForm(FlaskForm):
    username = StringField('', validators=[DataRequired()])
    password = PasswordField('', validators=[DataRequired()])
    submit = SubmitField('Sign In')