'''Views for Item Catalog App'''
import random
import string
import json
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask import make_response
from flask import g, session, jsonify
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import requests
from itemcatalog.models import Category, CatalogItem, User
from itemcatalog import utils
from . import app
from . import db


# Home page
@app.route('/')
@app.route('/welcome/')
@app.route('/home/')
@app.route('/index/')
def home():
    items = db.session.query(CatalogItem).all()
    cats = db.session.query(Category).all()
    return render_template('index.html', items=items, categories=cats)


@app.route('/login/')
def login():
    '''login page'''
    state = ''.join([random.choice(string.ascii_uppercase + string.digits)
                     for _ in xrange(32)])
    session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/logout/')
def logout():
    '''logout page'''
    provider = session.get('provider')
    if provider is not None:
        if provider == 'google':
            response = _gdisconnect()
        elif provider == 'facebook':
            response = _fbdisconnect()

        _clear_session()

        if response['status'] == '200':
            flash("You have been successfully logged out!")
        else:
            flash("An error ocurred when loggin out. Your browser session has been cleared!")
    else:
        flash('You were not logged in')

    return redirect('/')


# About page
@app.route('/about/')
def about():
    return render_template('about.html')


@app.route('/categories/')
def showCategories():
    '''Show all categories'''
    cats = db.session.query(Category).all()
    return render_template('categories.html', categories=cats)


@app.route('/category/<int:category_id>/')
def showCategoryItems(category_id):
    '''Show items for a given category id'''
    category = db.session.query(Category).filter_by(id=category_id).one()
    items = db.session.query(CatalogItem).filter_by(category_id=category.id)
    return render_template('category.html', category=category, items=items)


@app.route('/items/')
def showItems():
    '''Show all items'''
    items = db.session.query(CatalogItem).all()
    return render_template('allitems.html', items=items)

@app.route('/item/<int:id>/')
def showItem(id):
    '''Show a single item'''
    item = db.session.query(CatalogItem).filter_by(id=id).one()
    return render_template('item.html', item=item)


@app.route('/categories/new/', methods=('GET', 'POST'))
@utils.login_required
def newCategory():
    '''Create a new category'''
    if request.method == 'POST':
        category = Category(name=request.form['name'],
                            user_id=session['user_id'])
        db.session.add(category)
        db.session.commit()
        flash("New category %s created!" % category.name)
        return redirect(url_for('showCategoryItems', category_id=category.id))
    else:
        return render_template('newcategory.html')


@app.route('/category/<int:category_id>/new/', methods=['GET', 'POST'])
@utils.login_required
def newCatalogItem(category_id):
    '''Create a new item'''
    if request.method == 'POST':
        newItem = CatalogItem(
            name=request.form['name'],
            description=request.form['description'],
            category_id=category_id,
            user_id=session['user_id'])
        db.session.add(newItem)
        db.session.commit()
        flash("New catalog item %s created!" % newItem.name)
        return redirect(url_for('showCategoryItems', category_id=category_id))
    else:
        return render_template('newitem.html', category_id=category_id)


@app.route('/category/<int:category_id>/<int:item_id>/edit/',
           methods=('GET', 'POST'))
@utils.login_required
def editCatalogItem(category_id, item_id):
    '''Edit a catalog item'''
    editedItem = db.session.query(CatalogItem).filter_by(
        id=item_id, category_id=category_id).one()

    if editedItem.user_id != session['user_id']:
        flash("You are not authorized to edit this item!")
        return redirect(url_for('showCategoryItems', category_id=category_id))

    if request.method == 'POST':
        for attr in ('name', 'description', 'category_id'):
            if request.form[attr]:
                setattr(editedItem, attr, request.form[attr])
        db.session.commit()
        flash("Catalog item %s edited!" % editedItem.name)
        return redirect(url_for('showCategoryItems', category_id=category_id))
    else:
        categories = db.session.query(Category).all()
        return render_template(
            'editcatalogitem.html',
            category_id=category_id,
            item_id=item_id,
            item=editedItem,
            categories=categories)


@app.route('/category/<int:category_id>/<int:item_id>/delete/',
           methods=('GET', 'POST'))
@utils.login_required
def deleteCatalogItem(category_id, item_id):
    '''Delete a catalog item'''

    item = db.session.query(CatalogItem).filter_by(id=item_id).one()

    if item.user_id != session['user_id']:
        flash('You are not authorized to delete this item!')
        return redirect(url_for('showCategoryItems', category_id=category_id))

    if request.method == 'POST':
        name = item.name
        db.session.delete(item)
        db.session.commit()
        flash("Catalog item %s deleted!" % name)
        return redirect(url_for('showCategoryItems', category_id=category_id))
    else:
        return render_template('deletecatalogitem.html',
                               item=item)


# API end-points ===============================================================

@app.route('/categories/JSON/')
def getCategoriesJSON():
    '''API end-point to get all categories with items'''
    cats = db.session.query(Category).all()
    _cats = [c.serialize for c in cats]
    for _c in _cats:
        items = db.session.query(CatalogItem).filter_by(category_id=_c['id'])
        _c['items'] = [i.serialize for i in items]
    return jsonify(Categories=_cats)

@app.route('/category/<int:category_id>/JSON/')
def getCategoryItemsJSON(category_id):
    ''' API end-point to get items for a given category ID'''
    category = db.session.query(Category).filter_by(id=category_id).one()
    items = db.session.query(CatalogItem).filter_by(category_id=category.id)
    return jsonify(Category=[i.serialize for i in items])


# Authorization / Authentication ===============================================

@app.route('/gconnect', methods=['POST'])
@utils.check_state_token
def gconnect():
    ''' Connect with google Oauth2 API

    Taken from Udacity Authentication and Authorization Restaurant Menus example
    '''

    # Obtain authorization code
    auth_code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(auth_code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    client_id = json.loads(
        open('client_secrets.json', 'r').read())['web']['client_id']

    if result['issued_to'] != client_id:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_token = session.get('access_token')
    stored_gplus_id = session.get('gplus_id')
    if stored_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    utils.ggl_load_user_info(credentials)
    # If user doesn't exist, add to database
    utils.register_user()

    return render_template('login_welcome.html',
                           username=session['username'],
                           picture_url=session['picture'])


@app.route('/fbconnect', methods=['POST'])
@utils.check_state_token
def fbconnect():
    ''' Connect with facebook Oauth2 API

    Taken from Udacity Authentication and Authorization Restaurant Menus example
    '''

    access_token = request.data
    print "access token received %s " % access_token

    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # strip expire tag from access token
    token = result.split("&")[0]

    utils.fb_load_user_info(token)
    # If user doesn't exist, add to database
    utils.register_user()

    return render_template('login_welcome.html',
                           username=session['username'],
                           picture_url=session['picture'])


@app.route('/debug/session')
def _dump_session():
    ret = [session.keys(),
           { k: session.get(k) for k in ('username', 'user_id', 'gplus_id', 'email')}]
    return json.dumps(ret)

@app.route('/debug/clearsession/')
def _clear_session():
    session.clear()
    return redirect('/')


# Helper functions

# Disonnect with google Oauth2 API
# Revokes current user's token and resets their session
# Based on exmple from Udacity Authentication and Authorization Restaurant Menus
def _gdisconnect():
    # Only disconnect a connected user.
    access_token = session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'GDISCONNECT result', result
    return result


# Disonnect with facebook Oauth2 API
# Revokes current user's token and resets their session
# Based on example from Udacity Authentication and Authorization Restaurant Menus
def _fbdisconnect():
    facebook_id = session['facebook_id']
    # The access token must be included to successfully logout
    access_token = session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id,access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[0]
    print 'FBISCONNECT result', result
    return result
