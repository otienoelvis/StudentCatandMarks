from flask_wtf import FlaskForm
from wtforms import StringField,BooleanField, SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError
from pack.models import Admin, Student
from flask import flash
from flask_login import current_user


class StudentForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired()])
    registration_number = StringField('Admission No.', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit')


class AdminForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit')

    def validate_email(self, email):
        admin = Admin.query.filter_by(email=email.data).first()
        if admin:
            flash('That Email is taken.\nReset your password or use another email.')
            raise ValidationError('That Email is taken.\nReset your password or use another email.')


class LoginForm(FlaskForm):
    """
    login.html
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateProfileForm(FlaskForm):
    """
    profile.html
    """
    full_name = StringField('Full Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Update Info')

    def validate_full_name(self, full_name):
        """
        checks for duplicate
        :param full_name:
        """
        if full_name.data != current_user.full_name:
            admin = Admin.query.filter_by(full_name=full_name.data).first()
            if admin:
                flash('That name is taken.')
                raise ValidationError('That Email is taken.\nReset your password or use another name.')

    def validate_email(self, email):
        """
        checks for duplicate
        :param email:
        """
        if email.data != current_user.email:
            admin = Admin.query.filter_by(email=email.data).first()
            if admin:
                flash('That Email is taken.')
                raise ValidationError('That Email is taken.\nReset your password or use another email.')

