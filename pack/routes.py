from flask import render_template, redirect, url_for, flash, redirect, request, abort, Blueprint
from pack import app, db, bcrypt
from pack.forms import StudentRegister


# from pack.forms import StudentForm
# from pack.models import Student

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


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = StudentRegister()
    if form.validate_on_submit():
        flash(f"Account Created")
        return redirect(url_for('home'))
    return render_template("register.html", form=form)

