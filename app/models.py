
from . import db

class Person(db.Model):
    __table__ = 'persons'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(), nullable = False)
    age = db.Column(db.Integer(), nullable = False)
    email = db.Column(db.String(), unique = True, nullable = False)
    address = db.Column(db.String(), nullable = False)

    def __init__(self, name, age, email, address):
        self.name = name
        self.age = age
        self.email = email
        self.address = address 
    
    def __repr__(self):
        return f"{self.id}:{self.name}"