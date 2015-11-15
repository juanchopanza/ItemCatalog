# uncomment for sqlite database
#import os
#basedir = os.path.abspath(os.path.dirname(__file__))
#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'itemcatalog.db')

# Assumes DB named "itemcatalog" has been created
SQLALCHEMY_DATABASE_URI = 'postgresql:///itemcatalog'
DEBUG = True
SQLALCHEMY_ECHO = True
SECRET_KEY = '1234'
