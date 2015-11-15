#!/usr/bin/env python
import sys
import logging

activate_this = '/var/www/catalog/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))
sys.path.insert(0, '/var/www/catalog/')


from itemcatalog import app as application

logging.basicConfig(stream=sys.stderr)
application.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://catalog:<CATALOG_PWD>@localhost/itemcatalog'
application.config['DEBUG'] = True
application.config['SQLALCHEMY_ECHO'] = True
application.config['SECRET_KEY'] = '1234'
application.config['SECRETS_PATH'] = '/var/www/catalog/'
