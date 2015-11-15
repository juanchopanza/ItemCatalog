#!/usr/bin/env python

activate_this = '/var/www/catalog/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

from itemcatalog import app
import os

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///itemcatalog'
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 1234
if __name__ == '__main__':
    pass
    #basedir = os.path.abspath(os.path.dirname(__file__))
    #kapp.config.from_pyfile(config_file)
    #app.run(host='0.0.0.0', port=args.port)
