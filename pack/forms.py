from flask_wtf import FlaskForm
from wtforms import StringField,BooleanField, SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError
from pack.models import Admin, Student


class StudentForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired()])
    registration_number = StringField('Admission No.', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit')


class AdminForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired()])
    registration_number = StringField('Registration No.', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit')

    def validate_registration_number(self, registration_number):
        admin = Admin.query.filter_by(registration_number=registration_number.data).first()
        if admin:
            raise ValidationError('That Registration Number is already in the system.\nContact admin if you need help.')

    def validate_email(self, email):
        admin = Admin.query.filter_by(email=email.data).first()
        if admin:
            raise ValidationError('That Email is taken.\nReset your password or use another email.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')