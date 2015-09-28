import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'itemcatalog.db')
DEBUG = True
SQLALCHEMY_ECHO = True
SECRET_KEY = '1234'
