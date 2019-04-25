#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, url_for, \
    jsonify, make_response, session, flash
from flask_sqlalchemy import SQLAlchemy
from models import User, Category, Item
from oauth2client.client import credentials_from_clientsecrets_and_code
from functools import wraps
import random
import string
import httplib2
import json
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///catelogs.db'
db = SQLAlchemy(app)

CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())[
    'web']['client_id']
APPLICATION_NAME = "Item & Category APP"
STATE = ''.join(random.choice(string.ascii_uppercase + string.digits)
                for x in xrange(32))


# ************************************       Pre-defined Functions

def create_new_user(session):
    user = User(email=session['email'], avatar=session['picture'],
                username=session['username'])
    db.session.add(user)
    db.session.commit()
    ser = db.session.query(User).filter_by(email=session['email']).one()
    return user.id


def get_user_id(email):
    try:
        user = db.session.query(User).filter(User.email == email).one()
        return user.id
    except:
        return None


def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if 'user_id' in session:
            return fn(*args, **kwargs)
        else:
            flash("You have to login first to view the page.")
            return redirect('/')
    return wrapper


# ************************************       Controller - View

@app.route('/')
@app.route('/category')
@app.route('/categories')
def render_homepage():
    session['state'] = STATE
    categories = db.session.query(Category).all()
    latestItems = db.session.query(Item, Category, User)\
        .filter(Item.category_id == Category.id, Item.user_id == User.id)\
        .order_by("create_date desc").limit(15).all()
    return render_template('index.html', categories=categories,
                           items=latestItems, state=session['state'])


@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data

    try:
        credentials = credentials_from_clientsecrets_and_code(
                      'client_secrets.json',
                      ['https://www.googleapis.com/auth/drive.appdata',
                       'profile', 'email'],
                      code)
    except:
        response = make_response(json.dumps(
            'Error trying to exchange an authorization ' +
            'grant for an access token.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    check_result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if check_result.get('error') is not None:
        response = make_response(json.dumps(check_result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if check_result['user_id'] != gplus_id:
        response = \
            make_response(json.dumps(
                          "Token's user ID doesn't match given user ID."
                          ), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if check_result['issued_to'] != CLIENT_ID:
        response = \
            make_response(json.dumps(
                          "Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = session.get('access_token')
    stored_gplus_id = session.get('gplus_id')

    # Store the access token in the session for later use.
    session['access_token'] = credentials.access_token
    session['gplus_id'] = gplus_id
    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = answer.json()
    session['username'] = data['name']
    session['picture'] = data['picture']
    session['email'] = data['email']

    user_id = get_user_id(session['email'])
    if not user_id:
        user_id = create_new_user(session)

    session['user_id'] = user_id

    response = '''
      <img class="ui medium circular image" src="%s" alt="User Avatar">
      <div class="user-info">
      %s
      <a id="signoutButton" href="/gdisconnect">Sign out</a>
      </div>''' % (data['picture'], data['name'])

    return response


# For disconnecting from google plus
@app.route('/gdisconnect')
def gdisconnect():
    if session['email'] is None:
        response = make_response(json.dumps('Current user not connected.'),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        del session['username']
        del session['email']
        del session['picture']
        del session['state']
        del session['user_id']

        return redirect('/')


@app.route('/category/<int:category_id>')
def category_detail(category_id):
    category = db.session.query(Category).\
        filter(Category.id == category_id).one()
    categories = db.session.query(Category).all()
    category_items = db.session.query(Item, User) \
        .filter(Item.category_id == category_id, Item.user_id == User.id).all()
    return render_template('category.html', category=category,
                           categories=categories, items=category_items,
                           back=request.referrer, state=session['state'])


@app.route('/category/<int:category_id>/item/<int:item_id>')
def item_detail(category_id, item_id):
    category = db.session.query(Category).filter(Category.id == category_id)\
        .one()
    item = db.session.query(Item).filter(Item.id == item_id).one()
    return render_template('item.html', category=category, item=item,
                           back=request.referrer, state=session['state'])


@app.route('/category/<int:category_id>/item/<int:item_id>/edit',
           methods=['GET', 'POST'])
def item_edit(category_id, item_id):
    categories = db.session.query(Category).all()
    item = db.session.query(Item).filter(Item.id == item_id).one()
    permission = item.user_id == session['user_id']

    if request.method == 'POST':
        data = request.form
        if data['item-title']:
            item.title = data['item-title']
        if data['item-desc']:
            item.desc = data['item-desc']
        item.category_id = data['item-category']
        db.session.add(item)
        db.session.commit()
        flash("Edit Successfully!")
        return redirect(url_for('item_detail', category_id=item.category_id,
                                item_id=item.id))
    else:
        return render_template('edit.html', categories=categories, item=item,
                               back=request.referrer, permission=permission,
                               state=session['state'])


@app.route('/category/<int:category_id>/item/<int:item_id>/delete',
           methods=['GET', 'POST'])
def item_delete(category_id, item_id):
    item = db.session.query(Item).filter(Item.id == item_id).one()
    permission = item.user_id == session['user_id']

    if request.method == 'POST':
        db.session.delete(item)
        db.session.commit()
        flash("Delete Successfully!")
        return redirect(url_for('category_detail',
                                category_id=item.category_id))
    else:
        return render_template('delete.html', item=item, back=request.referrer,
                               permission=permission, state=session['state'])


@app.route('/item/new', methods=['GET', 'POST'])
@login_required
def item_add():
    categories = db.session.query(Category).all()

    if request.method == 'POST':
        data = request.form
        item = Item(
          title=data['item-title'],
          desc=data['item-desc'],
          category_id=data['item-category'],
          user_id=session['user_id'])
        db.session.add(item)
        db.session.commit()
        flash("New Item Added Successfully!")
        return redirect(url_for('category_detail',
                                category_id=data['item-category']))
    else:
        return render_template('new.html', categories=categories,
                               back=request.referrer, state=session['state'])


# ************************************       Controller - API

@app.route('/categories.json')
def api_categories():
    categories = db.session.query(Category).all()
    return jsonify(categories=[category.serialize for category in categories])


@app.route('/category/<int:category_id>.json')
def api_category_items(category_id):
    items = \
        db.session.query(Item).filter(Item.category_id == category_id).all()
    return jsonify(items=[item.serialize for item in items])


@app.route('/items.json')
def api_items():
    items = db.session.query(Item).all()
    return jsonify(items=[item.serialize for item in items])


@app.route('/item/<int:item_id>.json')
def api_item(item_id):
    items = db.session.query(Item).filter(Item.id == item_id).all()
    return jsonify(items=[item.serialize for item in items])


# ************************************       Start Server

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
