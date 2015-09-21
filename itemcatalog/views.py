'''Views for Item Catalog App'''
import random
import string
import json
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask import make_response
from flask import g
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import requests
from itemcatalog.models import Category, CatalogItem, User
from . import app
from . import db
from . import login_session


CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

# Home page
@app.route('/')
@app.route('/welcome/')
@app.route('/home/')
@app.route('/index/')
def home():
    return render_template('index.html')

# login page
@app.route('/login/')
def login():
    state = ''.join([random.choice(string.ascii_uppercase + string.digits)
                    for i in xrange(32)])
    login_session['state'] = state
    return render_template('login.html', STATE=state)


# About page
@app.route('/about/')
def about():
    return render_template('about.html')


# Show all categorys
@app.route('/categories/')
def showCategories():
    cats = db.session.query(Category).all()
    return render_template('categories.html', categories=cats)


# Show items for a given category
@app.route('/category/<int:category_id>/')
def showCategoryItems(category_id):
    category = db.session.query(Category).filter_by(id=category_id).one()
    items = db.session.query(CatalogItem).filter_by(category_id=category.id)
    return render_template('category.html', category=category, items=items)


# Show items for a given category
@app.route('/category/<category_name>/items/')
def showCategoryItemsFromName(category_name):
    category = db.session.query(Category).filter(Category.name.ilike(category_name)).one()
    items = db.session.query(CatalogItem).filter_by(category_id=category.id)
    return render_template('category.html', category=category, items=items)


# Show single item
@app.route('/category/<category_name>/<item_name>/')
def showItemFromNames(category_name, item_name):
    category = db.session.query(Category).filter(Category.name.ilike(category_name)).one()
    item = db.session.query(CatalogItem).filter_by(category_id=category.id,
                                                   name=item_name).one()
    return render_template('item.html', item=item)


# Show all items
@app.route('/items/')
def showItems():
    items = db.session.query(CatalogItem).all()
    return render_template('allitems.html', items=items)


# Create a new category
@app.route('/admin/categories/new/', methods=('GET', 'POST'))
def newCategory():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        category = Category(
            name=request.form['name'],
            user_id=login_session['user_id'])
        db.session.add(category)
        db.session.commit()
        flash("new category %s created!" % category.name)
        return redirect(url_for('showCategoryItems', category_id=category.id))
    else:
        return render_template('newcategory.html')


# Create a new item
@app.route('/admin/category/<int:category_id>/new/', methods=['GET', 'POST'])
def newCatalogItem(category_id):
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newItem = CatalogItem(
            name=request.form['name'],
            description=request.form['description'],
            category_id=category_id,
            user_id=login_session['user_id'])
        db.session.add(newItem)
        db.session.commit()
        flash("new catalog item %s created!" % newItem.name)
        return redirect(url_for('showCategoryItems', category_id=category_id))
    else:
        return render_template('newitem.html', category_id=category_id)


def _bad_user_alert(msg="You can't do this!"):
    '''Helper for unauthorized user actions'''
    script = """
    <script>
    function myFunction() {
    alert('Unauthorized User: %s');
    }
    </script>
    <body onload='myFunction()''>"""

    return script % msg


# Edit a catalog item
@app.route('/admin/category/<int:category_id>/<int:item_id>/edit/',
           methods=('GET', 'POST'))
def editCatalogItem(category_id, item_id):

    if 'username' not in login_session:
        return redirect('/login')

    editedItem = db.session.query(CatalogItem).filter_by(id=item_id, category_id=category_id).one()

    if editedItem.user_id != login_session['user_id']:
        return _bad_user_alert('You can only edit your own items.')

    if request.method == 'POST':
        for attr in ('name', 'description', 'price'):
            if request.form[attr]:
                setattr(editedItem, attr, request.form[attr])
        db.session.commit()
        flash("catalog item %s edited!" % editedItem.name)
        return redirect(url_for('showCategoryItems', category_id=category_id))
    else:
        return render_template(
            'editcatalogitem.html',
            category_id=category_id,
            item_id=item_id,
            item=editedItem)


# Delete a menu item
@app.route('/admin/category/<int:category_id>/<int:item_id>/delete/',
           methods=('GET', 'POST'))
def deleteCatalogItem(category_id, item_id):

    if 'username' not in login_session:
        return redirect('/login')

    item = db.session.query(CatalogItem).filter_by(id=item_id).one()

    if item.user_id != login_session['user_id']:
        return _bad_user_alert('You are not authorized to delete this item.')

    if request.method == 'POST':
        name = item.name
        db.session.delete(item)
        db.session.commit()
        flash("catalog item %s deleted!" % name)
        return redirect(url_for('showCategoryItems', category_id=category_id))
    else:
        return render_template('deletecatalogitem.html',
                               item=item)


# Connect with google Oauth2 API
# Taken from Udacity Authentication and Authorization Restaurant Menus example
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        print 'BAD STATE \n%s\n%s' % (request.args.get('state'), login_session['state'])
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
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
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['credentials'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # If user doesn't exist, add to database
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output



# Disonnect with google Oauth2 API
# Revokes current user's token and resets their login_session
# Taken from Udacity Authentication and Authorization Restaurant Menus example
@app.route('/gdisconnect/')
def gdisconnect():
    # Only disconnect a connected user.
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % credentials
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    print 'GDISCONNECT result', result
    if result['status'] == '200':
        # Reset the user's sesson.
        del login_session['credentials']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# User Helper Functions.
# Taken from Udacity Authentication and Authorization Restaurant Menus example.

def createUser(login_session):
    newUser = User(name=login_session['username'],
                   email=login_session['email'],
                   picture=login_session['picture'])
    db.session.add(newUser)
    db.session.commit()
    user = db.session.query(User).filter_by(email=login_session['email']).one()
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
