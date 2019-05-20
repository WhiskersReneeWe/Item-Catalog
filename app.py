#!/usr/bin/env/ python
# -*- coding: utf-8 -*-


from oauth2client.client import FlowExchangeError
from oauth2client.client import flow_from_clientsecrets
import requests
import httplib2
import json
import string
import random
from flask import session as login_session
from flask import (Flask,
                   render_template,
                   request,
                   url_for,
                   redirect,
                   jsonify,
                   make_response,
                   flash)

from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy import create_engine
from sqlalchemy.sql import func
from datetime import datetime
from db_setup import (Base,
                      User,
                      Category,
                      Item)

# Connect to Database and create database session
engine = engine = create_engine('sqlite:///ItemCatalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = scoped_session(DBSession)


app = Flask(__name__)

# backend codes with Users
def createUser(login_session):
    newUser = User(username = login_session['username'], email = login_session['email'])
    session.add(newUser)
    session.commit()

    user = session.query(User).filter_by(email = login_session['email']).one()
    return user.id

def getUserInfo(user_id):

    user = session.query(User).filter_by(id = user_id).one_or_none()
    print(user)
    return user

def getUserID(email):

    try:
        user = session.query(User).filter_by(email = email).one()
        return user.id
    except:
        return None


# homepage 
@app.route('/')
@app.route('/catalog')
def home():
    items = session.query(Item).limit(5).all()
    n_items = len(items)
    cates = session.query(Category).all()

    user = login_session.get('username')
    return render_template("home.html", cates=cates, items=items, n=n_items, user = user)




@app.route('/catalog/<cate_name>')
@app.route('/catalog/<cate_name>/items')
# @app.route('/<string: cate_name>/items')
def Showcateitems(cate_name):
    user = login_session.get('username')
    print(user)
    # get all catagories
    cates = session.query(Category).all()
    cate = session.query(Category).filter_by(name=cate_name).all()
    cate_id = 0
    for c in cate:
        cate_id = c.id

    items = session.query(Item).filter_by(category_id=cate_id).all()
    n_items = len(items)
    return render_template('Showcateitems.html', cates = cates, cate_name=cate_name, n=n_items, items=items, user = user)


@app.route('/catalog/<cate_name>/items/<int:item_id>/')
def desc(cate_name, item_id):

    item = session.query(Item).filter_by(id=item_id).one_or_none()
    cates = session.query(Category).filter_by(name = cate_name).all()
    
    if item == None or cates == None:
        response = make_response(json.dumps('Resource not found.'), 404)
        response.headers['Content-Type'] = 'application/json'
        return response
    
    # Get current user id
    currentUserid = getUserID(login_session['email'])

    for cate in cates:
        if cate.id == item.category_id:
            cate_name = cate.name

    
    return render_template('desc.html', item=item, user_id = currentUserid, categoryName = cate_name)


#Add button on the home page for users who signed in
@app.route('/catalog/add', methods=['GET', 'POST'])
def Addcateitem():
    # Check if user is logged in
    user_id = None
    email = login_session.get('email')
    if email:
        user = session.query(User).filter_by(email = email).first()
        if user:
            user_id = user.id

    else:
        return redirect('/signin')

    if request.method == 'POST':

        if not request.form['name']:
            flash('Please add the item name')
            return redirect(url_for('Addcateitem'))

        if not request.form['description']:
            flash('Please add an item description')
            return redirect(url_for('Addcateitem'))


        # Add category item
        newitem = Item(name = request.form['name'], description = request.form['description'], \
                       category_id = request.form['category'], user_id = user_id)
        session.add(newitem)
        session.commit()

        return redirect(url_for('home'))
    else:
        # Get all categories
        cates = session.query(Category).all()

        # Don't know how to make this html yet.
        return render_template('Addcateitem.html', cates = cates)

@app.route('/catalog/<cate_name>/items/<int:item_id>/edit', methods=['GET', 'POST'])
def Editcateitem(cate_name, item_id):
    # Check if user is logged in
    user_id = None
    email = login_session.get('email')
    if email:
        user = session.query(User).filter_by(email = email).first()
        if user:
            user_id = user.id

    else:
        return redirect('/signin')

    # Get category item
    item = session.query(Item).filter_by(id = item_id).first()
    item_cate = session.query(Category).filter_by(id = item.category_id).one_or_none()
    
    # Get user who created this item
    creator = getUserInfo(item.user_id)

    # Check if logged in user is the user who created this item
    if creator.id != user_id:
        print("Add your first item first")
        return render_template('Addcateitem.html', cates = cates)

    cates = session.query(Category).filter_by(name = cate_name).all()
    if request.method == 'POST':
        if request.form['name']:
            item.name = request.form['name']
        if request.form['description']:
            item.description = request.form['description']
        if request.form['category']:
            item.category_id = request.form['category']
        # how to store the editted item descriptions?
        session.add(item)
        session.commit()
        return redirect(url_for('Showcateitems', cate_name = item_cate.name ,item_id = item.id))
    else:
        return render_template('Editcateitem.html', cates = cates, item = item)


@app.route('/catalog/<cate_name>/items/<int:item_id>/delete', methods=['GET', 'POST'])
def Deleteitem(cate_name, item_id):
    # Check if user is logged in
    # Check if user is logged in
    user_id = None
    email = login_session.get('email')
    if email:
        user = session.query(User).filter_by(email = email).first()
        if user:
            user_id = user.id

    else:
        return redirect('/signin')

    # Get current item
    item = session.query(Item).filter_by(id = item_id).first()
    item_cate = session.query(Category).filter_by(id = item.category_id).one_or_none()

    # Get creator of item
    creator = getUserInfo(item.user_id)

    # Check if logged in user is creator of category item
    if creator.id != user_id:
        return redirect('/login')

    if request.method == 'POST':
        session.delete(item)
        session.commit()
        return redirect(url_for('Showcateitems', cate_name = cate_name))
    else:
        return render_template('Deleteitem.html', item = item, cate_name = item_cate)



@app.route('/signin')
def Showsignin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))

    login_session['state'] = state
    return render_template('signin.html', state=state, GOOGLE_CLIENT_ID=GOOGLE_CLIENT_ID)


@app.route('/gconnect', methods=['POST'])
def gconnect():

    # first check if login is messed up upon request
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    code = request.data

    try:
        oauth_flow = flow_from_clientsecrets('Client_Secret.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)

    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)

    h = httplib2.Http()
    response, content = h.request(url, 'GET')
    result = json.loads(content)

    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    google_id = credentials.id_token['sub']
    if result['user_id'] != google_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    


    if result['issued_to'] != GOOGLE_CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check if the current User is already connected
    stored_access_token = login_session.get('access_token')
    stored_google_id = login_session.get('google_id')
    if stored_access_token is not None and google_id == stored_google_id:
        response = make_response(json.dumps(
            'Current user is already logged in.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the session info for the user who logged in each time
    # Note: Every time a user logged in my web app page, a new session gets created
    login_session['access_token'] = credentials.access_token
    login_session['google_id'] = google_id

    # When in this new user login session, we grab this user's information
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()
    login_session['logged_in'] = True
    login_session['provider'] = 'google'
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    
    # First check if user in login session is in the database
    user = session.query(User).filter_by(email = data['email']).first()
    if not user:
        user = User(username = data['name'], email = data['email'])
        session.add(user)
        session.commit()

    # check all users that are in the database
    users = session.query(User).all()
    for u in users:
        print(u.email)
    ###### can delete this later##############



    msg = "Logged in successfully! You are now logged in as %s"
    flash(msg % login_session['username'])

    return render_template('login-success.html',
                           username=login_session['username'],
                           img_url=login_session['picture']
                           )

@app.route('/signout')
def signOut():
    access_token = None
    if 'access_token' in login_session:
        access_token = login_session['access_token']
    if access_token == None:
        print('Access Token is None')
        response = make_response(json.dumps(
            'Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response


    url = ('https://accounts.google.com/o/oauth2/revoke?token=%s'
           % login_session['access_token'])
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]



    del login_session['access_token']
    del login_session['logged_in']
    del login_session['google_id']
    del login_session['username']
    del login_session['email']
    del login_session['picture']
    del login_session['provider']
    flash("You have been logged out")

    return render_template('signout.html', GOOGLE_CLIENT_ID=GOOGLE_CLIENT_ID)

    



################# JSON Endpoints ##################
@app.route('/catalog/JSON')
def CatelogJSON():
    cates = session.query(Category).all()
    return jsonify(Categories = [cate.serialize for cate in cates])

@app.route('/catalog/<cate_name>/JSON')
@app.route('/catalog/<cate_name>/items/JSON')
def CateItemsJSON(cate_name):

    # Use the category name passed in to find the category id
    # Use this id to query Item table
    # I haven't figured out a more efficient way to do this yet
    cate = session.query(Category).filter_by(name=cate_name).all()
    cate_id = 0
    for c in cate:
        cate_id = c.id

    CateItems = session.query(Item).filter_by(category_id = cate_id).all()
    return jsonify(categoryItems = [item.serialize for item in CateItems])

@app.route('/catalog/<cate_name>/<item_name>/JSON')
def ItemDescJSON(cate_name, item_name):
    cate = session.query(Category).filter_by(name=cate_name).all()
    cate_id = 0
    for c in cate:
        cate_id = c.id

    item = session.query(Item).filter_by(category_id = cate_id, name = item_name).all()
    return jsonify(Item_info = [i.serialize for i in item])


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    GOOGLE_CLIENT_ID = json.loads(open('client_secret.json', 'r').read())[
        'web']['client_id']
    app.debug = True
    app.run(host="0.0.0.0", port=5000)
