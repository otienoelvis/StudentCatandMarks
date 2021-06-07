from flask_wtf import FlaskForm
from wtforms import StringField,BooleanField, SubmitField, PasswordField, IntegerField, FileField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError
from pack.models import Admin, Student
from flask import flash
from flask_login import current_user


class StudentForm(FlaskForm):
    full_name = StringField('Student Full Name', validators=[DataRequired()])
    admission_number = StringField('Admission Number', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')

    def validate_email(self, email):
        email = Student.query.filter_by(email=email.data).first()
        if email:
            flash('Another student has that email.\nContact Admin for help.')
            raise ValidationError('That Email is taken.\nReset your password or use another email.')

    def validate_admission_number(self, admission_number):
        student = Student.query.filter_by(admission_number=admission_number.data).first()
        if student:
            flash('Another student has that admission number.\n Check your form or contact site admin for help.')
            raise ValidationError('Another student has that admission number.\n Check your form or contact site admin for help.')


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
    submit = SubmitField('Update')

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


class UploadForm(FlaskForm):
    unit_code = StringField('Unit Code', validators=[DataRequired()])
    unit_name = StringField('Unit Name', validators=[DataRequired()])
    student_name = StringField('Student Name', validators=[DataRequired()])
    admission_number = StringField('Student Adm', validators=[DataRequired()])
    cat_1 = IntegerField('Cat 1', validators=[DataRequired()])
    cat_2 = IntegerField('Cat 2', validators=[DataRequired()])
    main_exam = IntegerField('Main Exam', validators=[DataRequired()])
    submit = SubmitField('Submit')


class UploadCsvForm(FlaskForm):
    csv_file = FileField('Choose file', validators=[DataRequired()])
    unit_code = StringField('Unit Code', validators=[DataRequired()])
    unit_name = StringField('Unit Name', validators=[DataRequired()])
    submit = SubmitField('Submit')



