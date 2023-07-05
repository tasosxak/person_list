
from . import db

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
    email = db.Column(db.String(), nullable = False)
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