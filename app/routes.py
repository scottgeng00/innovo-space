import sys

from app import app, db, socketio
from flask import Flask, render_template, url_for, flash, redirect, request
from flask_login import login_required, current_user

from app.views import main
from app.models import User

from datetime import datetime

from app.views.main import EditProfileForm

@app.before_request
def before_request():
      if current_user.is_authenticated:
            current_user.last_seen = datetime.utcnow()
            db.session.commit()


@app.route('/', methods=['GET', 'POST'])
def index():
  return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
  return main.login()

@app.route('/logout')
def logout():
  return main.logout()

@app.route('/about', methods=['GET', 'POST'])
def about():
  return render_template('about.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
  return main.register()

@app.route('/stinky', methods=['GET', 'POST'])
def stinky():
  return render_template('stinky.html')

@app.route('/forums', methods = ['GET', 'POST'])
def forums():
  return main.forums()

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        return redirect(url_for('user', username = current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)

@app.route('/user/<username>', methods=['GET','POST'])
@login_required
def user(username):
  user = User.query.filter_by(username=username).first_or_404()
  posts = [
    {'author': 'Dr. A', 'body': ' at 2:45 PM on 09/21/2020'},
    {'author': 'Dr. B', 'body': ' at 2:45 PM on 09/28/2020'}
  ]
  return render_template('user.html', user=user, posts = posts)


@app.route('/messages')
def messages():
    return render_template('session.html')

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)