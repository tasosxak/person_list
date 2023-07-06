from app.models import Person, Address
from app import db
from sqlalchemy import or_

def create_person(name, age, email, street_name, street_number):
    """
    Controller function for creating a new person record. 
    Adds a new person to the list with the provided name, age, email, street name and street number
    """

    # create a new address object
    address = Address(street_name=street_name, number=street_number)

    # create a new person object
    person = Person(name=name, age=age, email=email, address=address)
    
    # save the person and address objects to the database
    db.session.add(address)
    db.session.add(person)
    db.session.commit()

    return person

def get_persons(page=1, per_page=10, search_query=None):
    """
    Controller function for getting the list of persons with pagination support.
    Retrieves a paginated list of persons from the database 
    """

    # Query the database for paginated persons
    persons = Person.query.filter(or_(Person.name.ilike(f'%{search_query}%'), Person.email.ilike(f'%{search_query}%'))).paginate(page=page, per_page=per_page)
    #persons = Person.query.paginate(page=page, per_page=per_page)
    return persons

def update_person(person):
    """
    Controller function for updating an existing person record.
    Modifies the provided fields: name, age, street_name or/and street number
    """
    #person = Person.query.get(person_id)

    # update the fields if provided
    if person:
        """
        if name:
            person.name = name
        if age:
            person.age = age
        if street_name:
            person.address.street_name = street_name
        if street_number:
            person.address.number = street_number
        """
        db.session.commit() # commit the changes to the database
        return True
    return False
            
def delete_person(person_id):
    """
    Controller function for deleting an existing person record.
    Removes the specified person from the list.
    """
    person = Person.query.get_or_404(person_id)

    try:
        db.session.delete(person)
        db.session.commit()
        return True
    except:
        db.session.rollback()
        return False