from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from app import app, db, log_in
from .forms import LoginForm, RegisterForm
import jinja2
from app.models import User
import flask_login
from flask_login import login_required, login_user, logout_user, current_user

@app.route('/')
def home():
    return render_template('home.html', tite = 'Home')
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('home'))
    return render_template('login.html', title='Sign In', form=form)
    @app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))
