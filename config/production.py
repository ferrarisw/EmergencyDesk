import os

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, '../data.sqlite')

DEBUG = False
SECRET_KEY = 'top-secret!'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                          'sqlite:///' + db_path
GOOGLE_MAPS_API_KEY = 'AIzaSyDV40MOxLr9fo2G1BwxEaA6WBXpZa1Fnjs'
