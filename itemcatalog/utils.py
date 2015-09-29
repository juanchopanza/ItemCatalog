'''Helper utilities for itemcatalog app'''

from functools import wraps
import json
import httplib2
import requests
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


def register_user():
    '''Register a user in DB if not already registered'''
    user_id = getUserID(session['email'])
    if not user_id:
        user_id = createUser(session)
    session['user_id'] = user_id


def ggl_load_user_info(credentials):
    '''Loads user info into session

    Elements loaded:
        * username
        * email
        * picture
        * provider = 'google'
        * provider_id
    '''
    # Store the access token in the session for later use.
    session['provider'] = 'google'
    session['gplus_id'] = credentials.id_token['sub']
    session['access_token'] = credentials.access_token

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    username = data['name']
    session['username'] = username if username else 'Anonymous'
    session['picture'] = data['picture']
    session['email'] = data['email']


def fb_load_user_info(token):
    '''Loads user info into session

    Elements loaded:
        * username
        * email
        * picture
        * provider = 'facebook'
        * provider_id
    '''

    url = 'https://graph.facebook.com/v2.4/me?%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    data = json.loads(result)
    session['provider'] = 'facebook'
    session['facebook_id'] = data["id"]
    session['access_token'] = token.split('=')[1]

    session['username'] = data["name"]
    session['email'] = data["email"]

    # The token must be stored in the session in order to properly logout,
    # let's strip out the information before the equals sign in our token

    # Get user picture
    url = 'https://graph.facebook.com/v2.4/me/picture?%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    session['picture'] = data["data"]["url"]
