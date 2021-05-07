from flask import render_template, redirect, url_for, flash, redirect, request, abort, Blueprint
from pack import app, db, bcrypt
from pack.forms import StudentForm, AdminForm, LoginForm
from pack.models import Admin, Student
from flask_login import login_user


@app.route("/layout", methods=['GET', 'POST'])
def layout():
    return render_template("layout.html")


@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    return render_template("home.html")


@app.route("/user", methods=['GET', 'POST'])
def user_profile():
    return render_template("user.html")


@app.route("/tables", methods=['GET', 'POST'])
def table_list():
    return render_template("tables.html")


# noinspection PyUnresolvedReferences
@app.route("/admin_register", methods=['GET', 'POST'])
def register():
    form = AdminForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        admin = Admin(full_name=form.full_name.data,
                      registration_number=form.registration_number.data,
                      email=form.email.data,
                      password=hashed_password)
        db.session.add(admin)
        db.session.commit()
        flash("Account Created")
        return redirect(url_for('login'))
    return render_template("register.html", form=form)


@app.route("/adminlogin", methods=['GET', 'POST'])
def login():
    # if current_user.is_authenticated:
    # return redirect(url_for('main.home'))

    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(email=form.email.data).first()
        if admin and bcrypt.check_password_hash(admin.password, form.password.data):
            login_user(admin)
            # next_page = request.args.get('next')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

"""
    full_name = StringField('Full Name', validators=[DataRequired()])
    registration_number = StringField('Admission No.', validators=[DataRequired()])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    password = PasswordField(db.String(60), validators=[DataRequired(), EqualTo])
    confirm_password"""
