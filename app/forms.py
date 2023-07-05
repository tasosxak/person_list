from flask_wtf import FlaskForm, Form
from wtforms import StringField, IntegerField, SubmitField,FormField,EmailField
from wtforms.validators import DataRequired


class AddressForm(Form):
    street_name = StringField('Address Name', validators=[DataRequired('Please enter your street name')])
    number = IntegerField('Address Number', validators=[DataRequired('Please enter your street number')])

class PersonForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired('Please enter your name')])
    age = IntegerField('Age', validators=[DataRequired('Please enter your age')])
    email = EmailField('Email', validators=[DataRequired('Please enter your email address')])
    address = FormField(AddressForm)
    submit = SubmitField('Submit')