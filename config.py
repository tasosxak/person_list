
import os 

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'a super secret key !!!!!'

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DEV_DB_URL") or  'sqlite:///' + os.path.join(BASE_DIR,'database.db')

"""
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("DB_URL", 'sqlite:///' + os.path.join(BASE_DIR,'database.db'))
"""

CONFIG = {
    "default_config" : DevelopmentConfig
}

"""
DB_SETTINGS = { 
    'SQLALCHEMY_DATABASE_URI' : 'sqlite:///' + os.path.join(BASE_DIR,'database.db'),
    'SQLALCHEMY_TRACK_MODIFICATIONS' : False
}
"""