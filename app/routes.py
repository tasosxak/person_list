from app.forms import LoginForm, PersonForm
from . import create_app
from flask import render_template, request, flash, redirect, url_for
import os
from .controllers import *
from flask_login import current_user, login_required, logout_user

app = create_app(os.getenv('FLASK_CONFIG') or 'default_config')

"""
@app.errorhandler(wtforms.csrf.CSRFError)
def handle_csrf_error(e):
    return "CSRF Error - Invalid or missing CSRF token", 400
"""

@app.route('/persons/create', methods=['POST', 'GET'])
@login_required
def create_person_route():
	form = PersonForm()
	if request.method  == 'GET':
		return render_template('create_person.html', form=form)
	
	if request.method == 'POST':
		if form.validate_on_submit():
			res = create_person(form)
			if res['object']:
				flash(res['message'], 'success')
				return redirect(url_for('get_persons_route'))
			else:
				flash(res['message'], 'error')
				return render_template('create_person.html', form=form)
		else:
			flash('There are errors in the form. Please review and correct them.', 'error')
	return render_template('create_person.html', form=form)

@app.route('/persons', methods=['GET'])
@login_required
def get_persons_route():
	search_query = request.args.get('search', '') # get the search query from the request
	page = request.args.get('page', 1, type=int) # get the current page from the query parameters or default to 1
	per_page = 10 # set the number of items per page to 10

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
    
	if request.method == 'GET':
		return render_template('edit_person.html', form=form, person=person)
	
	if request.method == 'POST':
		if form.validate_on_submit():

			# update the person's data based on the form input 
			res = update_person(form,person)
			if res['object']:
				flash(res['message'], 'sucess')
				return redirect(url_for('get_persons_route'))    
			else:
				flash(res['message'], 'error')
				return render_template('edit_person.html', form=form, person=person)
		else:
			flash('There are errors in the form. Please review and correct them.', 'error')
			return render_template('edit_person.html', form=form, person=person)

@app.route('/persons/<int:person_id>/delete', methods=['POST'])
@login_required
def delete_person_route(person_id):
	
	res = delete_person(person_id) # delete the person if exists
	flash(res['message'], res['type'])

	return redirect(url_for('get_persons_route'))


@app.route('/login', methods=['GET', 'POST'])
def login():

	if current_user.is_authenticated:
		return redirect(url_for('get_persons_route'))

	form = LoginForm()

	if request.method == 'GET':
		return render_template('login.html', form=form)
	
	if request.method == 'POST':
		if form.validate_on_submit():
			res = authenticate_user(form)
			if res['object']:
				return redirect(url_for('get_persons_route'))
			else:
				return render_template('login.html', form=form, error=res['message'])
	
	return render_template('login.html', form=form)
	

@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('login'))


@app.route('/')
def home():
	if current_user.is_authenticated:
		return redirect(url_for('get_persons_route'))
	return redirect(url_for('login'))