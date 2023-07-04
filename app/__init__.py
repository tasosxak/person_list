from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import CONFIG 
from flask_migrate import Migrate


db = SQLAlchemy() # initializes the SQLAlchemy extension for db operations
migrate = Migrate() # initializes database migration functionallity

def create_app(config_name):
    # create Flask application instance 
    app = Flask(__name__, template_folder='templates')

    # load configuartion from CONFIG based on config_name
    app.config.from_object(CONFIG[config_name])

    # initialize application-specific configurations
    CONFIG[config_name].init_app(app)

    # initialize SQLAlchemy extension with the Flask app
    db.init_app(app)

    # initialize database migration functionality
    migrate.init_app(app, db)

    return app