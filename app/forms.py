"""
forms.py

This module defines Flask-WTF form classes used throughout the web application for user
authentication, password management, and event scheduling.

Forms included:

- LoginForm:
    Handles user login with email and password fields, enforcing length and format validation.

- SignUpForm:
    Manages user registration, including validation for strong passwords and email format,
    with a confirm-password check.

- ChangePasswordForm:
    Allows existing users to change their password securely, enforcing strength rules
    and matching confirmation.

- EventForm:
    Enables users to create or edit calendar events, with fields for title, description,
    time range, and privacy settings. Includes a custom validator to ensure end time is
    after start time.

All forms use appropriate WTForms validators for data integrity and security.
"""
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed,FileSize
from wtforms import StringField, PasswordField, SubmitField,TextAreaField, DateTimeLocalField, SelectField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp,DataRequired, ValidationError
from datetime import datetime

class LoginForm(FlaskForm):
    """
    Form for user login.

    Fields:
        email (StringField): User email. Required, must be valid and max 254 chars.
        password (PasswordField): User password. Required, 12–128 chars.
        submit (SubmitField): Submit button for the login form.
    """
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
    """
    Form for new user registration.

    Fields:
        username (StringField): Desired username. Required, 3–20 chars.
        email (StringField): User email. Required, must be valid.
        password (PasswordField): New password. Required, 12–128 chars, must contain:
            - at least one uppercase letter,
            - at least one lowercase letter,
            - at least one number.
        confirm_password (PasswordField): Must match the password.
        submit (SubmitField): Submit button for the sign-up form.
    """
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
    """
    Form for changing an existing user's password.

    Fields:
        oldPassword (PasswordField): The current password. Required, 12–128 chars.
        newPassword (PasswordField): The new password. Required, 12–128 chars, must contain:
            - at least one uppercase letter,
            - at least one lowercase letter,
            - at least one number.
        confirmNewPassword (PasswordField): Must match the new password.
    """
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
    """
    Form for creating or editing a calendar event.

    Fields:
        title (StringField): Title of the event. Required.
        description (TextAreaField): Optional event details.
        start_time (DateTimeLocalField): Start timestamp of the event. Required.
        end_time (DateTimeLocalField): End timestamp of the event. Required.
        privacy_level (SelectField): Visibility level of the event.
            Choices: 'private', 'friends', 'specific_users'.

    Methods:
        validate_end_time(field): Ensures end_time is later than start_time.
    """
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    
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
        'Privacy Level',
        choices=[
            ('private', 'Private'),
            ('friends', 'Friends'),
        ],
        validators=[DataRequired()]
    )

    def validate_end_time(form, field):
        if field.data <= form.start_time.data:
            raise ValidationError("End time must be after start time")