from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from app import app, db, log_in
from .forms import LoginForm, RegisterForm, CreatorSettings, MeetingForm
import jinja2
from app.models import User, Meeting
import flask_login
from flask_login import login_required, login_user, logout_user, current_user
from app.forms import CreatorSettings, DeleteForm
import calendar
import datetime
from datetime import time, datetime

@app.route('/')
def home():
    """ Home web page
                    
            Properties:
                 routes object to '/'
            Returns:
                 object with HTML file and 'Home' title
    """
    if current_user.is_active:
        return redirect(url_for('meetings'))       # Milestone 3 says to make the meetings page the default for logged in users


    today = datetime.today()
    year = today.year
    month = calendar.month_name[today.month]
    listofdays = calendar.monthcalendar(year, today.month)
    return render_template('home.html',year=year, month=month, 
                           listofdays=listofdays, 
                           title = 'Home')
    
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
        if int(form.Start.data.split(':')[0]) > int(form.End.data.split(':')[0]):
            flash('Error: Start time must be before End time')
            return redirect(url_for('settings'))

        user = User.query.filter_by(id=current_user.id).first()
        t = form.Duration.data.split(':')
        user.meeting_duration = time(int(t[0]), int(t[1]), int(t[2]))
        t = form.Start.data.split(':')
        user.availability_start = time(int(t[0]), int(t[1]), int(t[2]))
        t = form.End.data.split(':')
        user.availability_end = time(int(t[0]), int(t[1]), int(t[2]))

        db.session.add(user)
        db.session.commit()

        flash("Your settings have been updated")
        return redirect(url_for('home'))
    
    return render_template('settings.html', title = 'Account Settings', form = form)

@app.route('/meetings')
def meetings():
    M = Meeting.query.all()
    Yours = []
    for m in M:
        if m.user_id == current_user.id:
            Yours.append(m)

    return render_template('meetings.html', title = 'Creator Home', meets = Yours)

@app.route('/<username>')
def profile(username):
    today = datetime.today()
    year = today.year
    month = calendar.month_name[today.month]
    listofdays = calendar.monthcalendar(year, today.month)
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
    return render_template('profile.html', title = 'Creator Profile', 
                           year=year, month=month, listofdays=listofdays, 
                           user = user)
    
@app.route('/delete',methods=['GET','POST'])
@login_required
def delete():
    if not current_user.is_authenticated:
        flash('Please Log in as creator to delete user')
        return redirect(url_for('login')) 
    form=DeleteForm()
    if form.validate_on_submit():
        user= User.query.filter_by(id=form.ids.data).first()
        db.session.delete(user)
        db.session.commit()
        flash(f'User {user.username} successfully deleted! ')
        return redirect(url_for('home'))
    return render_template('delete.html',title='Delete User',form=form)


@app.route('/search_users')
def search_users():
    users = User.query.all()
    return render_template('search_users.html', title = 'Account Settings', users = users)


@app.route('/book/<username>/<year>/<month>/<day>', methods=['GET', 'POST'])
def book(username, year, month, day):
    user = User.query.filter_by(username=username).first()
    form = MeetingForm()
    times = []
    start = str(user.availability_start)
    end = str(user.availability_end)
    start = start.split(':')[0]
    end = end.split(':')[0]
    for i in range(int(end)):
        if i >= int(start):
            if i < 10:
                item = '0' + str(i) + ':00:00'
                times.append([item, item])
            else:
                item = str(i) + ':00:00'
                times.append([item, item])
    form.startTime.choices = times

    if month == 'January':
        num_Month = 1
    if month == 'February':
        num_Month = 2
    if month == 'March':
        num_Month = 3
    if month == 'April':
        num_Month = 4
    if month == 'May':
        num_Month = 5
    if month == 'June':
        num_Month = 6
    if month == 'July':
        num_Month = 7
    if month == 'August':
        num_Month = 8
    if month == 'September':
        num_Month = 9
    if month == 'October':
        num_Month = 10
    if month == 'November':
        num_Month = 11
    if month == 'December':
        num_Month = 12
    
    if form.validate_on_submit():
        start = form.startTime.data.split(':')[0]
        date_time = datetime(int(year), num_Month, int(day), int(start))
        m = Meeting(description = form.description.data, time = date_time, guest = form.Guest.data, user_id = user.get_id())
        db.session.add(m)
        db.session.commit()
        flash("Meeting Confirmed")

    return render_template('book.html',title='Book a Meeting', user=user, year=year, month=month, day=day, form = form)

@app.route('/delete_meeting_<id>',methods=['GET','POST'])
def delete_meeting(id):
    meet = Meeting.query.filter_by(id=id).first()
    db.session.delete(meet)
    db.session.commit()
    return redirect(url_for('meetings'))

