from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import CONFIG 
from flask_migrate import Migrate

from flask_login import LoginManager


db = SQLAlchemy() # initializes the SQLAlchemy extension for db operations
migrate = Migrate() # initializes database migration functionallity

def create_app(config_name):
    # create Flask application instance 
    app = Flask(__name__, template_folder='templates')

    

    # load configuartion from CONFIG based on config_name
    app.config.from_object(CONFIG[config_name])

    #csrf = CSRFProtect(app)

    # initialize application-specific configurations
    CONFIG[config_name].init_app(app)

    # initialize SQLAlchemy extension with the Flask app
    db.init_app(app)

    from .models import User
    login_manager = LoginManager(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        # Implement the logic to load a user from the database
        # Return the User object associated with the given user_id
        user = User.query.filter_by(id=user_id).first()
        return user

    # initialize database migration functionality
    migrate.init_app(app, db)

    return app

