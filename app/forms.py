"""
WTForms for Hilltop Tea application.

Provides form classes with Bootstrap styling for all user input.
"""

from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, SelectField, IntegerField,
    FloatField, TextAreaField, DateField, SubmitField, BooleanField
)
from wtforms.validators import (
    DataRequired, Length, EqualTo, NumberRange, Optional, ValidationError
)
from app.models import User, Employee, UserRole, EmployeeGroup


class LoginForm(FlaskForm):
    """Form for user login."""

    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login', render_kw={'class': 'btn btn-primary w-100'})


class UserForm(FlaskForm):
    """Form for creating/editing users."""

    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=3, max=80),
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=6, max=255),
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    role = SelectField('Role', choices=[
        (UserRole.ADMIN.value, 'Administrator'),
        (UserRole.GM.value, 'General Manager'),
        (UserRole.SUPERVISOR.value, 'Supervisor')
    ], validators=[DataRequired()])
    submit = SubmitField('Save User', render_kw={'class': 'btn btn-primary'})

    def validate_username(self, field):
        """Validate that username is unique."""
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already exists.')


class UserEditForm(FlaskForm):
    """Form for editing users (password optional)."""

    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=3, max=80),
    ])
    role = SelectField('Role', choices=[
        (UserRole.ADMIN.value, 'Administrator'),
        (UserRole.GM.value, 'General Manager'),
        (UserRole.SUPERVISOR.value, 'Supervisor')
    ], validators=[DataRequired()])
    password = PasswordField('New Password (leave blank to keep current)', validators=[Optional()])
    submit = SubmitField('Update User', render_kw={'class': 'btn btn-primary'})


class EmployeeForm(FlaskForm):
    """Form for creating/editing employees."""

    name = StringField('Full Name', validators=[
        DataRequired(),
        Length(min=2, max=100),
    ])
    group = SelectField('Group', choices=[
        (EmployeeGroup.PRODUCTION.value, 'Production'),
        (EmployeeGroup.WRAPPING.value, 'Wrapping')
    ], validators=[DataRequired()])
    active = BooleanField('Active', default=True)
    submit = SubmitField('Save Employee', render_kw={'class': 'btn btn-primary'})


class ProductionEntryForm(FlaskForm):
    """Form for daily production entry (dynamic fields)."""

    submit = SubmitField('Save Production Records', render_kw={'class': 'btn btn-primary'})


class PaymentForm(FlaskForm):
    """Form for recording payments."""

    amount = FloatField('Amount (₦)', validators=[
        DataRequired(),
        NumberRange(min=0.01, message='Amount must be greater than 0')
    ])
    payment_date = DateField('Payment Date', validators=[DataRequired()])
    notes = TextAreaField('Notes', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Record Payment', render_kw={'class': 'btn btn-primary'})


class PayrollFilterForm(FlaskForm):
    """Form for filtering payroll data."""

    year = SelectField('Year', coerce=int, validators=[DataRequired()])
    month = SelectField('Month', coerce=int, validators=[DataRequired()])
    group = SelectField('Group', choices=[
        ('', 'All Groups'),
        (EmployeeGroup.PRODUCTION.value, 'Production'),
        (EmployeeGroup.WRAPPING.value, 'Wrapping')
    ], validators=[Optional()])
    submit = SubmitField('Filter', render_kw={'class': 'btn btn-outline-secondary'})


class ChangePasswordForm(FlaskForm):
    """Form for changing user password."""

    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[
        DataRequired(),
        Length(min=6, max=255),
    ])
    confirm_password = PasswordField('Confirm New Password', validators=[
        DataRequired(),
        EqualTo('new_password', message='Passwords must match')
    ])
    submit = SubmitField('Change Password', render_kw={'class': 'btn btn-primary'})
