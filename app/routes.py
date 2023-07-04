from . import create_app
from flask import render_template
import os

app = create_app(os.getenv('FLASK_CONFIG') or 'default_config')

@app.route('/')
def home():
	return render_template('index.html')
