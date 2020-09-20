from flask import render_template, url_for, flash, redirect, request
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField, TextAreaField, PasswordField, BooleanField, validators
from wtforms.validators import ValidationError, DataRequired, EqualTo, Email, Length
from wtforms.fields.html5 import DateField
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user
from app.models import User
from app import db

class loginForm(FlaskForm):
    username = StringField('Username: ', validators=[DataRequired()], default=None)
    password = PasswordField('Password: ', validators=[DataRequired()], default=None)
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class registrationForm(FlaskForm):
    username = StringField('Set Username: ', validators=[DataRequired()], default=None)
    password = PasswordField('Set Password: ', validators=[DataRequired()], default=None)
    passwordV = PasswordField('Confirm Password: ', validators=[DataRequired(),EqualTo('password')], default=None)
    email = StringField('Email: ', validators=[Email()])
    utype = SelectField(u'Who are you?*', choices=[(0, 'Patient'), (1, 'Doctor'), (2, 'Volunteer')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('An account with that username already exists.')

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired()])
    about_me = TextAreaField('About me', validators = [Length(min=0, max=250)])
    submit = SubmitField('Submit')

def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = loginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            password = form.password.data

            if user is None or not user.check_password(form.password.data):
                flash('Invalid username or password')
                return redirect(url_for('login'))

            login_user(user, remember=form.remember_me.data)

            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)

    return render_template('login.html', form=form)

def logout():
    logout_user()
    return redirect(url_for('index'))


def register():
    form = registrationForm()
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        if form.validate_on_submit():

            username = form.username.data
            password = form.password.data
            email = form.email.data
            utype = form.utype.data

            u = User(username=username, email=email, user_type=utype)
            u.set_password(password)
            db.session.add(u)
            db.session.commit()

            flash('Congratulations, you are now a registered user! Please login to continue.')
            return redirect(url_for('login'))

                #add stuff to store salted_hash into Azure database
                #return render_template('registration.html', form = form, congrats = "Registration successful! Taking you to your home page.")
                #take user to user home page
    return render_template('registration.html', form=form)

def forums():
    return render_template('forum.html')