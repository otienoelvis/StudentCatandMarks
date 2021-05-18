"""
routes
"""
from flask import render_template, jsonify, redirect, url_for, flash, redirect, request, abort, Blueprint, send_file
from pack import app, db, bcrypt
from pack.forms import StudentForm, AdminForm, LoginForm, UpdateProfileForm, UploadCsvForm
from pack.models import Admin, Unit
from flask_login import login_user, current_user, logout_user, login_required
import json
from io import TextIOWrapper
import csv


def serializer(field):
    """
    serializer
    :param field:
    :return:
    """
    return {
        "unit_code": field.unit_code,
        "unit_name": field.unit_name,
        "student_name": field.student_name,
        "admission_number": field.admission_number,
        "cat_1": field.cat_1,
        "cat_2": field.cat_2,
        "main_exam": field.main_exam
    }


@app.route("/homes", methods=['GET', 'POST'])
@login_required
def homes():
    """
    renders home page
    :return:
    """
    data = jsonify([*map(serializer, Unit.query.all())])
    return data


@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
@login_required
def home():
    """
    renders home page
    :return:
    """
    # page = request.args.get('page', 1, type=int)
    # posts = Unit.query.order_by(Unit.date_added.desc()).paginate(page=page, per_page=20)
    posts = Unit.query.all()
    return render_template("home.html", title='Home', navbar_title='Dashboard', posts=posts)


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
        flash('Your profile has been updated!')
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
    form = UploadCsvForm()

    if request.method == 'POST':
        csv_file = request.files.getlist('file')
        for file in csv_file:
            file = TextIOWrapper(file, encoding='utf-8')
            csv_reader = csv.reader(file, delimiter=',')
            next(csv_reader)
            for row in csv_reader:
                # noinspection PyUnboundLocalVariable

                unit_code = request.form.get('unit_code')
                unit_name = request.form.get('unit_name')
                student_name = row[0]
                admission_number = row[1]
                cat_1 = float(row[2])
                cat_2 = float(row[3])
                main_exam = float(row[4])
                total = ((cat_1 + cat_2) / 2) + main_exam

                if total >= 70:
                    grade = 'A'
                elif total >= 60:
                    grade = 'B'
                elif total >= 50:
                    grade = 'C'
                elif total >= 40:
                    grade = 'D'
                else:
                    grade = 'F'

                marks = Unit(unit_code=unit_code,
                             unit_name=unit_name,
                             student_name=student_name,
                             admission_number=admission_number,
                             cat_1=cat_1,
                             cat_2=cat_2,
                             main_exam=main_exam,
                             total=total,
                             grade=grade
                             )
                db.session.add(marks)
                db.session.commit()
        flash('File has been submitted successfully')
        return redirect(url_for('upload_csv'))
    return render_template('upload.html', form=form)


@app.route('/download')
@login_required
def downloadfile():
    """
    download csv template
    :return:
    """
    path = "D:\MyProjects\Student\pack\static\csv_template\example.csv"
    return send_file(path, as_attachment=True)


@app.route("/table", methods=['GET', 'POST'])
@login_required
def table():
    """
    renders home page
    :return:
    """
    return render_template("table.html", title='Home', navbar_title='Dashboard')
