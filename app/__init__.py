from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import CONFIG 
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name):
    app = Flask(__name__, template_folder='templates')
    app.config.from_object(CONFIG[config_name])
    CONFIG[config_name].init_app(app)
    
    db.init_app(app)
    migrate.init_app(app, db)

    return app