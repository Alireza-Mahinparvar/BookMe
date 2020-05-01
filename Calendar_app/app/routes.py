from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from app import app, db, log_in
from .forms import LoginForm, RegisterForm, CreatorSettings
import jinja2
from app.models import User
import flask_login
from flask_login import login_required, login_user, logout_user, current_user

@app.route('/')
def home():
    """ Home web page
                    
            Properties:
                 routes object to '/'
            Returns:
                 object with HTML file and 'Home' title
    """
    if current_user.is_authenticated:
        return redirect(url_for('meetings'))
    
    return render_template('home.html', tite = 'Home')
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    """ Logs in user
                    
            Properties:
                 routes object to '/login' data sent from browser to server          
                 
            Attributes:
                 forms: object with LoginForms                 
                 user: username typed in            
                 
            Returns:
                 object with HTML file and 'Sign In' title       
                 if authenticated: redirected to home page
                 if successfully validated: redirected to home page
                 if unsuccessfully validated: Exception String thrown and redirected to login page           
    """
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

@app.route('/register', methods=['GET', 'POST'])
def register():
    """ Registers user to database
                    
            Properties:
                 routes object to '/register' data sent from browser to server
                 
            Attributes:
                 forms: object with RegisterForms    
                 user: username typed in         
                 
            Returns:
                 object with HTML file and 'Sign Up' title      
                 if authenticated: redirected to home page
                 if successfully validated: creates user, adds to database, then redirects to login page        
    """
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created')
        return redirect(url_for('login'))
    return render_template('register.html', title='Sign Up', form=form)

@app.route('/logout')
def logout():
    '''Logs Out User    
    
            Properties:
                 routes object to '/logout              
            Returns:
                 redirects to Home page            
    '''
    logout_user()
    return redirect(url_for('home'))

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    form = CreatorSettings()
    if not current_user.is_active:
        flash("You must be logged in to edit your account settings")
        return redirect(url_for('home'))
    if form.validate_on_submit():
        flash("Your settings have been updated")
    return render_template('settings.html', title = 'Account Settings', form = form)

@app.route('/meetings')
def meetings():

    return render_template('meetings.html', title = 'Creator Home')

@app.route('/<username>')
def profile(username):
    if current_user.is_active:
        flash("Only guests may view other creators' profiles")
        return redirect(url_for('home'))
    found = False
    name = username
    users = User.query.all()
    for u in users:
        if name == u.username:
            found = True
            user = u
    if not found:
        flash('User "' + name + '" Not Found')
        return redirect(url_for('home'))
    return render_template('profile.html', title = 'Creator Profile', user = user)



