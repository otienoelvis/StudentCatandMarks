"""
routes
"""
from flask import render_template, redirect, url_for, flash, redirect, request, abort, Blueprint
from pack import app, db, bcrypt
from pack.forms import StudentForm, AdminForm, LoginForm, UpdateProfileForm, UploadForm
from pack.models import Admin, Unit
from flask_login import login_user, current_user, logout_user, login_required

from io import TextIOWrapper
import csv


@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
@login_required
def home():
    """
    renders home page
    :return:
    """
    return render_template("home.html", title='Home', navbar_title='Dashboard')


# noinspection PyUnresolvedReferences,PyArgumentList
@app.route("/register", methods=['GET', 'POST'])
def register():
    """
    registers user
    :return:
    """
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = AdminForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        admin = Admin(full_name=form.full_name.data,
                      email=form.email.data,
                      password=hashed_password)
        db.session.add(admin)
        db.session.commit()
        flash("Account Created successfully.")
        return redirect(url_for('login'))
    return render_template("register.html", form=form, title='Admin Signup')


@app.route("/login", methods=['GET', 'POST'])
def login():
    """
    login user
    :return:
    """
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(email=form.email.data).first()
        if admin and bcrypt.check_password_hash(admin.password, form.password.data):
            login_user(admin, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('Login Success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password')
    return render_template('login.html', title='Admin Login', form=form)


@app.route("/logout")
def logout():
    """
    logsout user
    :return:
    """
    logout_user()
    return redirect(url_for('login'))


@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    """
    render profile page & handles user info update
    :return:
    """
    form = UpdateProfileForm()
    if form.validate_on_submit():
        current_user.full_name = form.full_name.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.full_name.data = current_user.full_name
        form.email.data = current_user.email

    return render_template("profile.html", form=form, title='User Profile', navbar_title='My Profile')


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        current_user.full_name = form.full_name.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.full_name.data = current_user.full_name
        form.email.data = current_user.email
    return render_template('profile.html', title='User Profile', navbar_title='My Profile', form=form)


@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_csv():
    """
    uploads csv and saves to db
    """
    form = UploadForm()
    if request.method == 'POST':
        csv_file = request.files['file']
        csv_file = TextIOWrapper(csv_file, encoding='utf-8')
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            # noinspection PyUnboundLocalVariable
            marks = Unit(unit_code=row[0],
                         unit_name=row[1],
                         student_name=row[2],
                         student_id=row[3],
                         cat_1=row[4],
                         cat_2=row[5],
                         cat_3=row[6],
                         main_exam=row[7])
            db.session.add(marks)
            db.session.commit()
            flash('Your account has been updated!')
        return redirect(url_for('upload_csv'))
    return """
            <form method='post' action='' enctype='multipart/form-data'>
              Upload a csv file: <input type='file' name='file'>
              <input type='submit' value='Upload'>
            </form>
           """


"""
    full_name = StringField('Full Name', validators=[DataRequired()])
    registration_number = StringField('Admission No.', validators=[DataRequired()])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    password = PasswordField(db.String(60), validators=[DataRequired(), EqualTo])
    confirm_password"""
