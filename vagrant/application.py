#!/usr/bin/env python3

from flask import Flask, render_template, request, redirect, url_for, flash
from flask import jsonify, make_response
from flask import session as login_session
from sqlalchemy import create_engine, desc, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

engine = create_engine('sqlite:///beermenuwithusers.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/login')
# Create anti-forgery state token
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
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
    result = json.loads(str(h.request(url, 'GET')[1].decode('utf-8')))
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

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
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
            'Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # See if a user exists, if it doesn't make a new one
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
    print("done!")
    return output


# User Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
        # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        # Reset the user's sesson.
        del login_session['access_token']
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


@app.route('/')
@app.route('/index')
def index():
    # Check if user is logged in
    if 'username' not in login_session:
        categories = session.query(Category).order_by(asc(Category.name)).all()
        items = session.query(Item).order_by(desc(Item.id)).limit(7)
        return render_template('publicindex.html', categories=categories,
                               items=items)
    else:  # user logged in
        user_id = getUserID(login_session['email'])
        categories = session.query(Category).order_by(asc(Category.name)).all()
        items = session.query(Item).filter_by(
            user_id=user_id).order_by(desc(Item.id)).limit(7)
        return render_template('index.html', categories=categories,
                               items=items)


@app.route('/catalog/<category_id>/items/', methods=['GET', 'POST'])
def showItemsOfCategory(category_id):
    # Check if user is logged in
    if 'username' not in login_session:
        headertype = 'publicheader.html'
        categories = session.query(Category).order_by(asc(Category.name)).all()
        category = session.query(Category).filter_by(id=category_id).one()
        counts = session.query(Item).filter_by(cat_id=category_id).count()
        items = session.query(Item).filter_by(cat_id=category_id).all()
        return render_template('catalog.html', headertype=headertype,
                               categories=categories, category=category,
                               n=counts, items=items)
    else:  # user logged in
        headertype = 'header.html'
        user_id = getUserID(login_session['email'])
        categories = session.query(Category).filter_by(
            user_id=user_id).order_by(asc(Category.name)).all()
        counts = session.query(Item).filter_by(
            cat_id=category_id, user_id=user_id).count()
        try:  # check if user has made at least one category entry
            category = session.query(Category).filter_by(
                id=category_id, user_id=user_id).one()
        except:
            category = None
        items = session.query(Item).filter_by(
            cat_id=category_id, user_id=user_id).all()

        return render_template('catalog.html', headertype=headertype,
                               categories=categories, category=category,
                               n=counts, items=items)


@app.route('/catalog/<category_id>/<item_id>/')
def itemDescription(item_id, category_id):
    # Query database
    item = session.query(Item).filter_by(id=item_id).one()

    # Check if user is logged in
    if 'username' not in login_session:
        return render_template('publicitem.html', item=item)
    else:
        return render_template('item.html', item=item)


# JSON APIs to view Item Description
@app.route('/catalog/<category_id>/<item_id>/JSON')
@app.route('/catalog/<category_id>/<item_id>/json')
def itemDescriptionJSON(category_id, item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    return jsonify(item=item.serialize)


@app.route('/additem', methods=['GET', 'POST'])
def addItem():
    # Check if user is logged in
    if 'username' not in login_session:
        return redirect('/login')

    # Query database
    categories = session.query(Category).order_by(asc(Category.name)).all()
    items = session.query(Item).all()
    error = None

    if request.method == 'POST':
        if request.form['title'] != "":

            # Get Category Name for selected category via Category ID
            category_id = request.form['category_dropdown']
            category_name = session.query(Category).filter_by(id=category_id).one().name
            user_id = getUserID(login_session['email'])
            new_item = Item(name=request.form['title'],
                            description=request.form['description'],
                            cat_id=request.form['category_dropdown'],
                            user_id=user_id)   
            session.add(new_item)
            session.commit()

            return redirect(url_for('index'))
        else:
            error = 'Sorry, You have to chose a Name for Your Beer!'

    return render_template('additem.html', categories=categories, error=error)


@app.route('/addcategory', methods=['GET', 'POST'])
def addCategory():
    # Check if user is logged in
    if 'username' not in login_session:
        return redirect('/login')

    error = None

    if request.method == 'POST':
        if request.form['title'] != "":

            user_id = getUserID(login_session['email'])
            new_cateogry = Category(name=request.form['title'],
                                    user_id=user_id)
            session.add(new_cateogry)
            session.commit()

            return redirect(url_for('index'))
        else:
            error = 'Sorry, You have to chose a Name for the Category!'

    return render_template('addcategory.html', error=error)


@app.route('/catalog/<item_id>/edit', methods=['GET', 'POST'])
def editItem(item_id):
    # Check if user is logged in
    if 'username' not in login_session:
        return redirect('/login')

    # Query database
    categories = session.query(Category).order_by(asc(Category.name)).all()
    error_user = None
    error_title = None
    # Find item
    item = session.query(Item).filter_by(id=item_id).one()
    category_id = session.query(Item).filter_by(id=item_id).one().cat_id
    category = session.query(Category).filter_by(id=category_id).one()

    # Change Item
    if request.method == 'POST':
        # Check if title is not empty
        if request.form['title'] != "":
            # check if item to edit is created by user
            if item.user_id == getUserID(login_session['email']):
                item.name = request.form['title']
                item.description = request.form['description']
                # Change category via category_id
                category_id = request.form['category_dropdown']
                category_newname = session.query(Category).filter_by(
                    id=category_id).one().name
                category.name = category_newname
                session.add(item)
                session.add(category)
                session.commit()
                return redirect(url_for('index'))
            else:
                error_user = 'Sorry, You are only allowed to edit your own items'

        else:
            error_title = 'Sorry, You have to Chose a Name for Your Beer!'

    return render_template('edititem.html', item=item,
                           categories=categories, error_title=error_title, error_user=error_user)


@app.route('/catalog/<item_id>/delete', methods=['GET', 'POST'])
def deleteItem(item_id):
    error_user = None
    if 'username' not in login_session:
        return redirect('/login')
    item = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        # check if item to edit is created by user
        if item.user_id == getUserID(login_session['email']):
            session.delete(item)
            session.commit()
            return redirect(url_for('index'))
        else:
                error_user = 'Sorry, You are only allowed to delete your own items!'
                return render_template('deletetitem.html', error_user=error_user, item=item)
    else:
        return render_template('deletetitem.html', error_user=error_user, item=item)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
