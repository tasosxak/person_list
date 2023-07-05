from . import create_app
from flask import render_template, request, flash, redirect, url_for
import os
from .controllers import *
import wtforms

app = create_app(os.getenv('FLASK_CONFIG') or 'default_config')

"""
@app.errorhandler(wtforms.csrf.CSRFError)
def handle_csrf_error(e):
    return "CSRF Error - Invalid or missing CSRF token", 400
"""

@app.route('/persons', methods=['POST'])
def create_person_route():
	name = request.form.get('name')
	age = request.form.get('age')
	street_name = request.form.get('street-name')
	street_number = request.form.get('street_number')
	email = request.form.get('email')
	person = create_person(name, age, email, street_name, street_number)
	if person:
		flash('Person created successfully!', 'success')
		return redirect(url_for('home'))
	else:
		flash('Failed to create person.', 'error')
		return render_template('create_person.html')

@app.route('/persons', methods=['GET'])
def get_persons_route():
	page = request.args.get('page', 1, type=int)
	per_page = 10
	persons = get_persons(page,per_page)

	return render_template('persons.html', persons=persons)


@app.route('/persons/<int:person_id>', methods=['PUT'])
def update_person_route(person_id):
    name = request.form.get('name')
    age = request.form.get('age')
    street_name = request.form.get('street-name')
    street_number = request.form.get('street-number')
    res = update_person(person_id, name, age, street_name, street_number)

    return render_template('person.html', person=person)

@app.route('/persons/<int:person_id>', methods=['POST','DELETE'])
def delete_person_route(person_id):
	
	if  delete_person(person_id):
		flash('Person deleted successfully!', 'success')
		return redirect(url_for('home'))
	else:
	    flash('Failed to delete person.', 'error')
	    return redirect(url_for('home'))

@app.route('/')
def home():
	return render_template('index.html')