'''Views for Item Catalog App'''
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask import g
from itemcatalog.models import Category, CatalogItem
from . import app
from . import db

# TODO add routes


# Home page
@app.route('/')
@app.route('/welcome')
@app.route('/home')
@app.route('/index')
def home():
    return render_template('index.html')


# About page
@app.route('/about')
def about():
    return render_template('about.html')


# Show all restaurants
@app.route('/categories/')
def showRestaurants():
    cats = db.session.query(Category).all()
    return render_template('categories.html', categories=cats)

