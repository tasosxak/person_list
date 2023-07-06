from app.forms import LoginForm, PersonForm
from . import create_app
from flask import render_template, request, flash, redirect, url_for
import os
from .controllers import *
from flask_login import current_user, login_required, logout_user
from loguru import logger

app = create_app(os.getenv('FLASK_CONFIG') or 'default_config')

"""
@app.errorhandler(wtforms.csrf.CSRFError)
def handle_csrf_error(e):
    return "CSRF Error - Invalid or missing CSRF token", 400
"""

@app.route('/persons/create', methods=['POST', 'GET'])
@login_required
def create_person_route():

	logger.info("Received request to add a new person")

	form = PersonForm()
	if request.method  == 'GET':
		logger.info("Rendering create_person.html template")
		return render_template('create_person.html', form=form)
	
	if request.method == 'POST':
		if form.validate_on_submit():
			res = create_person(form)
			if res['object']:
				flash(res['message'], 'success')
				logger.info("Redirecting to person list after person creation")
				return redirect(url_for('get_persons_route'))
			else:
				flash(res['message'], 'error')
				logger.warning("Failed to create person")
				return render_template('create_person.html', form=form)
		else:
			flash('There are errors in the form. Please review and correct them.', 'error')
			logger.warning("Form validation failed")

	return render_template('create_person.html', form=form)

@app.route('/persons', methods=['GET'])
@login_required
def get_persons_route():
	search_query = request.args.get('search', '') # get the search query from the request
	page = request.args.get('page', 1, type=int) # get the current page from the query parameters or default to 1
	per_page = 10 # set the number of items per page to 10

	logger.info("Received request to get persons. Search query: {}".format(str(search_query)))

	# get paginated list of persons with optional search query
	persons = get_persons(page,per_page , search_query)
	
	return render_template('list_person.html', persons=persons)


@app.route('/persons/<int:person_id>/edit', methods=['POST', 'GET'])
@login_required
def update_person_route(person_id):
    
	# retrieve the existing person from the database
	person = Person.query.get_or_404(person_id)

	# create a form instance and populate it with existing person's data
	form  = PersonForm(obj=person)

	logger.info("Received request to update person with ID: {}".format(str(person_id)))
    
	if request.method == 'GET':
		logger.info("Rendering edit_person.html template for person with ID: {}".format(str(person_id)))
		return render_template('edit_person.html', form=form, person=person)
	
	if request.method == 'POST':
		if form.validate_on_submit():

			# update the person's data based on the form input 
			res = update_person(form,person)
			if res['object']:
				flash(res['message'], 'sucess')
				logger.info("Person with ID {} updated successfully".format(person_id))
				return redirect(url_for('get_persons_route'))    
			else:
				flash(res['message'], 'error')
				logger.warning("Failed to update person with ID {}: {}".format(person_id, res['message']))
				return render_template('edit_person.html', form=form, person=person)
		else:
			flash('There are errors in the form. Please review and correct them.', 'error')
			logger.warning("Validation errors encountered while updating person with ID: {}".format(person_id))
			return render_template('edit_person.html', form=form, person=person)

@app.route('/persons/<int:person_id>/delete', methods=['POST'])
@login_required
def delete_person_route(person_id):
	logger.info("Received request to delete person with ID: {}".format(person_id))
	res = delete_person(person_id) # delete the person if exists
	flash(res['message'], res['type'])
	logger.info("Deletion of person with ID {}: {}".format(person_id, res['message']))
	return redirect(url_for('get_persons_route'))


@app.route('/login', methods=['GET', 'POST'])
def login():
	logger.info("User login initiated")
	if current_user.is_authenticated:
		logger.warning("User is already authenticated, redirecting to get_persons_route")
		return redirect(url_for('get_persons_route'))

	form = LoginForm()

	if request.method == 'GET':
		return render_template('login.html', form=form)
	
	if request.method == 'POST':
		if form.validate_on_submit():
			res = authenticate_user(form)
			if res['object']:
				logger.info("User login successful, redirecting to get_persons_route")
				return redirect(url_for('get_persons_route'))
			else:
				logger.warning("User login failed: {}".format(res['message']))
				return render_template('login.html', form=form, error=res['message'])
			
	logger.warning("Invalid form submission, rendering login template")
	return render_template('login.html', form=form)
	

@app.route('/logout')
@login_required
def logout():
	logger.info("User logout initiated")
	logout_user()
	logger.info("User logout successful")
	return redirect(url_for('login'))


@app.route('/')
def home():
	if current_user.is_authenticated:
		return redirect(url_for('get_persons_route'))
	return redirect(url_for('login'))