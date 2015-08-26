'''Views for Item Catalog App'''
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask import g
from restaurantmenu.models import Restaurant, MenuItem
from . import app
from . import db

# TODO add routes
