"""Blogly application."""

import os

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///blogly')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True


@app.get('/')
def homepage():
    '''Redirect homepage'''

    return redirect('/users')


@app.get('/users')
def get_users():
    '''Populates user page with users in database'''

    users = User.query.all()

    return render_template('users.html', users=users)


@app.get('/users/new')
def new_user():
    '''Renders new user form'''

    return render_template('new.html')


@app.post('/users/new')
def create_user():
    '''Adds new user to database & redirects to users page'''

    first_name = request.form.get('first')
    last_name = request.form.get('last')
    img_url = request.form.get('imgURL')

    if img_url == '':
        img_url = None
    else:
        img_url = request.form.get('imgURL')

    new_user = User(first_name=first_name,
                    last_name=last_name, image_url=img_url)

    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')


@app.get('/users/<int:user_id>')
def user_details(user_id):
    '''Renders user detail page'''

    user = User.query.get(user_id)

    return render_template('details.html', user=user)


@app.post('/users/<int:user_id>/delete')
def delete_user(user_id):
    '''Deletes user from database'''

    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')


@app.get('/users/<int:user_id>/edit')
def get_edit_page(user_id):
    '''renders page to edit user data'''

    user = User.query.get(user_id)

    return render_template('edit.html', user=user)


@app.post('/users/<int:user_id>/edit')
def edit_user(user_id):
    '''updates user data in database'''

    user = User.query.get(user_id)

    first_name = request.form.get('first')
    last_name = request.form.get('last')
    img_url = request.form.get('imgURL')

    if img_url == '':
        img_url = None
    else:
        img_url = request.form.get('imgURL')

    user.first_name = first_name
    user.last_name = last_name
    user.image_url = img_url

    db.session.commit()

    return redirect('/users')


connect_db(app)
