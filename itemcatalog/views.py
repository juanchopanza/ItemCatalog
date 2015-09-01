'''Views for Item Catalog App'''
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask import g
from itemcatalog.models import Category, CatalogItem
from . import app
from . import db

# TODO add routes


# Home page
@app.route('/')
@app.route('/welcome/')
@app.route('/home/')
@app.route('/index/')
def home():
    return render_template('index.html')


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
    if request.method == 'POST':
        category = Category(name=request.form['name'])
        db.session.add(category)
        db.session.commit()
        flash("new category %s created!" % category.name)
        return redirect(url_for('showCategoryItems', category_id=category.id))
    else:
        return render_template('newcategory.html')


# Create a new item
@app.route('/admin/category/<int:category_id>/new/', methods=['GET', 'POST'])
def newCatalogItem(category_id):
    if request.method == 'POST':
        newItem = CatalogItem(
            name=request.form['name'],
            description=request.form['description'],
            category_id=category_id)
        db.session.add(newItem)
        db.session.commit()
        flash("new catalog item %s created!" % newItem.name)
        return redirect(url_for('showCategoryItems', category_id=category_id))
    else:
        return render_template('newitem.html', category_id=category_id)



# Edit a catalog item
@app.route('/admin/category/<int:category_id>/<int:item_id>/edit/',
           methods=('GET', 'POST'))
def editCatalogItem(category_id, item_id):
    editedItem = db.session.query(CatalogItem).filter_by(id=item_id, category_id=category_id).one()
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
    item = db.session.query(CatalogItem).filter_by(id=item_id).one()
    if request.method == 'POST':
        name = item.name
        db.session.delete(item)
        db.session.commit()
        flash("catalog item %s deleted!" % name)
        return redirect(url_for('showCategoryItems', category_id=category_id))
    else:
        return render_template('deletecatalogitem.html',
                               item=item)
