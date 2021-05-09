from datetime import datetime
from pack import db, login_manager
import pytz
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))


learners = db.Table('learners',
                    db.Column('student_id', db.Integer, db.ForeignKey('student.student_id')),
                    db.Column('unit_id', db.Integer, db.ForeignKey('unit.unit_id'))
                    )


class Student(db.Model):
    student_id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(50), nullable=False)
    registration_number = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.now(pytz.timezone('Africa/Nairobi')))

    subscriptions = db.relationship('Unit', secondary=learners, backref=db.backref('subscribers'), lazy='dynamic')

    def __repr__(self):
        return f"Student('{self.full_name}', '{self.registration_number}', '{self.email}')"


class Admin(db.Model, UserMixin):
    admin_id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.now(pytz.timezone('Africa/Nairobi')))

    units = db.relationship('Unit', backref='author', lazy=True)  # one to many r/ship to Unit table

    def __repr__(self):
        return f"Admin('{self.full_name}', '{self.registration_number}', '{self.email}')"

    def get_id(self):
        return self.admin_id

class Unit(db.Model):
    unit_id = db.Column(db.Integer, primary_key=True)
    unit_code = db.Column(db.String(50), nullable=False, unique=True)
    unit_name = db.Column(db.String(50), nullable=False, unique=True)
    cat_1 = db.Column(db.Integer, nullable=False, default=0)
    cat_2 = db.Column(db.Integer, nullable=False, default=0)
    cat_3 = db.Column(db.Integer, nullable=False, default=0)
    main_exam = db.Column(db.Integer, nullable=False, default=0)
    date_added = db.Column(db.DateTime, default=datetime.now(pytz.timezone('Africa/Nairobi')))

    admin_id = db.Column(db.Integer, db.ForeignKey('admin.admin_id'), nullable=False)  # one to many r/ship from Admin table

    def __repr__(self):
        return f"Unit('{self.unit_code}', '{self.unit_name}', '{self.cat_1}', '{self.cat_2}', '{self.cat_3}', '{self.main_exam}')"

