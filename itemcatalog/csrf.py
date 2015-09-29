'''CSRF helper functions

Based on Dan Jacob's flask snippet http://flask.pocoo.org/snippets/3/
'''

import string
import random
from flask import session, request, abort
from . import app


@app.before_request
def csrf_protect():
    '''Checks CSRF session token.

    Checks for POST, PUT and DELETE methods. Each request results
    in a new token being generated.

    If the request does not contain a form, checks are performed on
    the request arguments.

    In case of failure, calls flask.abort(302)
    '''
    if request.method in ("POST", "PUT", "DELETE"):
        csrf_token = session.pop('_csrf_token', None)
        data = request.form if request.form else request.args
        app.logger.debug('Request args %s', request.args)
        app.logger.debug('Request form %s', request.form)
        app.logger.debug('CSRF TOKENS \n%s\n%s',
                         data.get('_csrf_token'),
                         csrf_token)
        if not csrf_token or csrf_token != data.get('_csrf_token'):
            abort(403)


def gen_csrf_token():
    '''Return a random string composed of digits and upper case letters'''
    return ''.join([random.choice(string.ascii_uppercase + string.digits)
                     for _ in xrange(32)])

def get_csrf_token():
    '''Get session CSRF token

    Generates a new one if one not already in session
    '''
    if '_csrf_token' not in session:
        session['_csrf_token'] = gen_csrf_token()
    return session['_csrf_token']


# Add as global function csrf_token() in jinja templates
app.jinja_env.globals['csrf_token'] = get_csrf_token
