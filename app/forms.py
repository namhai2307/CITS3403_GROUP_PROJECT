from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed,FileSize
from wtforms import StringField, PasswordField, SubmitField,TextAreaField, DateTimeLocalField, SelectField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp,DataRequired, ValidationError
from datetime import datetime

class LoginForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(),
            Length(max=254),  
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=12, max=128),
        ]
    )
    submit = SubmitField('Login')

class SignUpForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Length(min=3, max=20),
        ]
    )
    email = StringField('Email', validators=[  # Add email field
        DataRequired(),
        Email()
    ])
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=12, max=128),
            Regexp('^(?=.*[A-Z]).*', message='Password must contain an uppercase letter.'),
            Regexp('^(?=.*[a-z]).*', message='Password must contain a lowercase letter.'),
            Regexp('^(?=.*[0-9]).*', message='Password must contain a number.'),
        ]
    )
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(),
            EqualTo('password', message="Passwords must match.")
        ]
    )
    submit = SubmitField('Sign Up')

class ChangePasswordForm(FlaskForm):
    oldPassword = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=12, max=128),
        ]
    )
    newPassword = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=12, max=128),
            Regexp('^(?=.*[A-Z]).*', message='Password must contain an uppercase letter.'),
            Regexp('^(?=.*[a-z]).*', message='Password must contain a lowercase letter.'),
            Regexp('^(?=.*[0-9]).*', message='Password must contain a number.'),
        ]
    )
    confirmNewPassword = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(),
            EqualTo('password', message="Passwords must match.")
        ]
    )


class EventForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    
    # Using HTML5's timestamp local type
    start_time = DateTimeLocalField(
        'Start Time',
        format='%Y-%m-%dT%H:%M',
        validators=[DataRequired()],
        render_kw={"type": "datetime-local"}
    )
    
    end_time = DateTimeLocalField(
        'End Time', 
        format='%Y-%m-%dT%H:%M',
        validators=[DataRequired()],
        render_kw={"type": "datetime-local"}
    )
    
    
    
    privacy_level = SelectField(
        'Sharing',
        choices=[
            ('private', 'Private'),
            ('friends', 'Friends'),
            ('specific_users', 'Specific Users')
        ],
        default='private'
    )

    def validate_end_time(form, field):
        if field.data <= form.start_time.data:
            raise ValidationError("End time must be after start time")