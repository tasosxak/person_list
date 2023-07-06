from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.models import Person, Address, User
from app import db
from sqlalchemy import or_
from flask_login import login_user
from loguru import logger

def create_person(form):
    """
    Controller function for creating a new person record. 
    Adds a new person to the list with the provided name, age, email, street name and street number
    """
    name = form.name.data
    age = form.age.data
    street_name = form.address.street_name.data
    street_number = form.address.number.data
    email = form.email.data

    # create a new address object
    address = Address(street_name=street_name, number=street_number)

    # create a new person object
    person = Person(name=name, age=age, email=email, address=address)
    
    # save the person and address objects to the database
    try:
        db.session.add(address)
        db.session.add(person)
        db.session.commit()
        logger.info('Person {} added successfully in the database.'.format(person.name))
        return {'object': person, "message": 'Person created successfully!'}
    except IntegrityError as e:
        db.session.rollback()
        #error_message = str(e)
        logger.warning("Email already exists for person {}".format(person.name))
        # error that there is already a person using the same email address
        return {'object': None, "message": "Email already exists. Please choose a different email."}
    except SQLAlchemyError as e:
        logger.error(f"Failed to add {person.name} in the database: {str(e)}")
        return {'object': None, "message": "Something went wrong :/"}

def get_persons(page=1, per_page=10, search_query=None):
    """
    Controller function for getting the list of persons with pagination support.
    Retrieves a paginated list of persons from the database 
    """

    try:
        # Query the database for paginated persons
        persons = Person.query.filter(or_(Person.name.ilike(f'%{search_query}%'), Person.email.ilike(f'%{search_query}%'))).paginate(page=page, per_page=per_page)
        #persons = Person.query.paginate(page=page, per_page=per_page)
        logger.info("Paginated persons retrieved successfully")
        return persons
    except Exception as e:
        logger.error("Failed to retrieve paginated persons: {}".format(str(e)))
        return None

def update_person(form, person):
    """
    Controller function for updating an existing person record.
    Modifies the provided fields: name, age, street_name or/and street number
    """
    if person:
        # assign the form data to the attributes of the person
        form.populate_obj(person)
        try:
            db.session.commit() # commit the changes to the database
            logger.info("Person {} updated successfully".format(person.name))
            return  {'object': person, 'message' :'{}\'s data updated sucessfully!'.format(person.name)}
        except IntegrityError:
            db.session.rollback()
            # error that there is already a person using the same email address
            logger.warning("Email already exists for person {}".format(person.name))
            return {'object': None, "message": "Email already exists. Please choose a different email."}
        except SQLAlchemyError as e:
            logger.error("Failed to update person {} in the database: {}".format(person.name, str(e)))
            return {'object': None, "message": "Something went wrong :/"}
        
    return { 'object': None, 'message': 'Failed to update {}\'s data :('.format(person.name)}
            
def delete_person(person_id):
    """
    Controller function for deleting an existing person record.
    Removes the specified person from the list.
    """
    person = Person.query.get_or_404(person_id)

    try:
        db.session.delete(person)
        db.session.commit()
        logger.info("Person {} deleted successfully".format(person.name))
        return {'message': 'Person deleted successfully!', 'type': 'success'}
    except:
        db.session.rollback()
        logger.error("Failed to delete person {} from the database: {}".format(person.name, str(e)))
        return {'message': 'Failed to delete person.', 'type': 'error'}
    

def authenticate_user(form):
    """
    Controller function for verifying user credentials and logging the user in
    """
    username = form.username.data
    password = form.password.data 

    user = User.query.filter_by(username=username).first()
    if user and user.password == password: # simple plain password check
        login_user(user)
        logger.info("User {} logged in successfully".format(user.username))
        return {'object': user, 'message': 'The user logged in successfully', 'type': 'success'}
    else:
         logger.warning("Invalid username or password")
         return {'object': user, 'message': 'Invalid username or password', 'type': 'error'}