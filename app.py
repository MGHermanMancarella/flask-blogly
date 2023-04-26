"""Blogly application."""

import os

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, User, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///blogly')  # TODO: change db url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True


@app.get('/')
def homepage():

    return redirect('/users')

@app.get('/users')
def get_users():
    
    users = User.query.all() #TODO: revisit if doesn't work

    return render_template('users.html', users=users)

@app.get('/users/new')
def new_user():

    return render_template('new.html')

@app.post('/users/new')
def create_user():

    first_name = request.forms.get('first')
    last_name = request.forms.get('last')
    img_url = request.forms.get('imgURL')

    new_user = User(first_name=first_name, last_name=last_name,image_url=img_url)

    db.session.add(new_user)    
    db.session.commit()

    return redirect('/users')

@app.get('users/<int: user_id>')
def user_details(user_id):

    user = User.query.get(user_id)

    return render_template('details.html', user=user)

@app.get('users/<int: user_id>/edit')
def get_edit_page(user_id):

    user = User.query.get(user_id)

    return render_template('edit.html', user=user)

@app.post('users/<int: user_id>/edit')
def edit_user(user_id):

    user = User.query.get(user_id)

    first_name = request.form.get('first')
    last_name = request.form.get('last')
    img = request.form.get('imgURL')

    user.first_name = first_name
    user.last_name = last_name
    user.image_url = img
 
    db.session.commit()

    return render_template('edit.html', user=user)


connect_db(app)
