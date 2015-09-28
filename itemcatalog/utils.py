'''Helper utilities for itemcatalog app'''

from functools import wraps
from flask import session, request, redirect, url_for, flash
from .models import User
from . import db


def login_required(f):
    '''Decorator to protect pages requiring login

    Adapted from flask view decorators tutorial

    * http://flask.pocoo.org/docs/0.10/patterns/viewdecorators/

    Redirects to login page.
    '''
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('The page you visited requires you to be logged in!')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


# User Helper Functions.
# Taken from Udacity Authentication and Authorization Restaurant Menus example.

def createUser(session):
    newUser = User(name=session['username'],
                   email=session['email'],
                   picture=session['picture'])
    db.session.add(newUser)
    db.session.commit()
    user = db.session.query(User).filter_by(email=session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = db.session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = db.session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None
