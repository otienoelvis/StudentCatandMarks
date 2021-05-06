from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired


class StudentRegister(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired()])
    registration_number = StringField('Admission No.', validators=[DataRequired()])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    submit = SubmitField('Submit')

"""
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(50), nullable=False)
    registration_number = db.Column(db.String(25), unique=True, nullable=False)
    phone_number = db.Column(db.String(14), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.now(pytz.timezone('Africa/Nairobi')))
"""