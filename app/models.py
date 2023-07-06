
from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id  = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)



class Address(db.Model):
    __tablename__ = 'address'
    id = db.Column(db.Integer, primary_key=True)
    street_name = db.Column(db.String(), nullable=False)
    number = db.Column(db.Integer, nullable=False)

    def __init__(self, street_name, number):
        self.street_name = street_name
        self.number = number

class Person(db.Model):
    __tablename__ = 'person'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(), nullable = False)
    age = db.Column(db.Integer(), nullable = False)
    email = db.Column(db.String(), unique=True, nullable = False)
    #address = db.Column(db.String(), nullable = False)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id', ondelete='CASCADE'), nullable=False)
    address = db.relationship('Address', backref='person', uselist=False, cascade="all,delete")

    def __init__(self, name, age, email, address):
        self.name = name
        self.age = age
        self.email = email
        self.address = address
    
    def __repr__(self):
        return f"{self.id}:{self.name}"