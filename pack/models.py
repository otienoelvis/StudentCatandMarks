from datetime import datetime
from pack import db
import pytz


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(50), nullable=False)
    registration_number = db.Column(db.String(25), unique=True, nullable=False)
    phone_number = db.Column(db.String(14), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.now(pytz.timezone('Africa/Nairobi')))

    def __repr__(self):
        return f"Student('{self.full_name}', '{self.registration_number}', '{self.phone_number}')"


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(14), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.now(pytz.timezone('Africa/Nairobi')))

    units = db.relationship('Unit', backref='author', lazy=True)  # one to many r/ship to Unit table 

    def __repr__(self):
        return f"Admin('{self.full_name}', '{self.phone_number}')"


class Unit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unit_code = db.Column(db.String(50), nullable=False, unique=True)
    unit_name = db.Column(db.String(50), nullable=False, unique=True)
    cat_1 = db.Column(db.Integer, nullable=False, default=0)
    cat_2 = db.Column(db.Integer, nullable=False, default=0)
    cat_3 = db.Column(db.Integer, nullable=False, default=0)
    main_exam = db.Column(db.Integer, nullable=False, default=0)
    date_added = db.Column(db.DateTime, default=datetime.now(pytz.timezone('Africa/Nairobi')))

    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)  # one to many r/ship from Admin table

    def __repr__(self):
        return f"Unit('{self.unit_code}', '{self.unit_name}', '{self.cat_1}', '{self.cat_2}', '{self.cat_3}', '{self.main_exam}')"



