#!/usr/bin/env python
import sys
import os
import logging

VENV = '/var/www/catalog'

activate_this = '%s/bin/activate_this.py' % VENV
execfile(activate_this, dict(__file__=activate_this))
os.environ['SECRETS_PATH'] = '%s/.secrets' % VENV

from itemcatalog import app as application

logging.basicConfig(stream=sys.stderr)
application.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://catalog:<CATALOG_PWD>@localhost/itemcatalog'
application.config['DEBUG'] = True
application.config['SQLALCHEMY_ECHO'] = True
application.config['SECRET_KEY'] = '1234'
