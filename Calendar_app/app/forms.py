from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TimeField, SelectField, DateField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError, NumberRange
from wtforms.fields.html5 import EmailField 
from .models import User
from app.models import Meeting
import datetime
from datetime import time

class LoginForm(FlaskForm):
    """ Holds Login Forms for Sign In webpage
           
           Args:
                 Flaskform: imported from flask_wtf            
                 
            Attributes:
                 username: Title for username textbox in webpage 
                 password: Title for password textbox in webpage
                 remember_me: Title for remember_me textbox in webpage
                 submit: Title for submit textbox in webpage   
                 
    """
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegisterForm(FlaskForm):
    """Holds Register Forms for Sign Up webpage
                        
             Args:
                 Flaskform: imported from flask_wtf     
                        
            Attributes:
                 username: Title for username textbox in webpage
                 email: Title for email textbox in webpage            
                 password: Title for password textbox in webpage       
                 confirmPassword: Title for password confirmation textbox in webpage             
                 submit: Title for submit textbox in webpage 
                 
    """
    username = StringField('Username', validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired(), Email(message="Please enter a valid email address")])
    password = PasswordField('Password', validators=[DataRequired()])
    confirmPassword = PasswordField('Reenter Password', validators=[DataRequired(), EqualTo("password", message="Passwords did not match")])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        """ Validates if user is in database
        
            Args:
                 username: object in question for verification
            Returns:
                 If in use: Validation Error String  
                 
        """
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username is already in use; choose another.')
 
    def validate_email(self, email):
        """ Validates if email is in database
        
            Args:
                 user: object in question for verification
            Returns:
                 If in use: Validation Error String  
                 
        """
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email is already in use; choose another.')


class CreatorSettings(FlaskForm):
    Duration = SelectField('Meeting Duration: ', choices=[(time(0, 15, 0), '15 minutes'), (time(0, 30, 0), '30 minutes'), (time(1, 0, 0), '1 hour')], validators=[DataRequired()])
    Start = SelectField('Availability Start Time', 
        choices= [('00:00:00', '12:00 AM'), ('01:00:00', '1:00 AM'), ('02:00:00', '2:00 AM'), (3, '3:00 AM'), (4, '4:00 AM'),
            (5, '5:00 AM'), (6, '6:00 AM'), (7, '7:00 AM'), (8, '8:00 AM'), (9, '9:00 AM'),
            (10, '10:00 AM'), (11, '11:00 AM'), (12, '12:00 PM'), (13, '1:00 PM'), (14, '2:00 PM'),
            (15, '3:00 PM'), (16, '4:00 PM'), (17, '5:00 PM'), (18, '6:00 PM'), (19, '7:00 PM'),
            (20, '8:00 PM'), (21, '9:00 PM'), (22, '10:00 PM'), (23, '11:00 PM')])
    End = SelectField('Availability End Time', 
        choices= [('0', '12:00 AM'), ('1', '1:00 AM'), ('2', '2:00 AM'), ('3', '3:00 AM'), ('4', '4:00 AM'),
            (5, '5:00 AM'), (6, '6:00 AM'), (7, '7:00 AM'), (8, '8:00 AM'), (9, '9:00 AM'),
            (10, '10:00 AM'), (11, '11:00 AM'), (12, '12:00 PM'), (13, '1:00 PM'), (14, '2:00 PM'),
            (15, '3:00 PM'), (16, '4:00 PM'), (17, '5:00 PM'), (18, '6:00 PM'), (19, '7:00 PM'),
            (20, '8:00 PM'), (21, '9:00 PM'), (22, '10:00 PM'), (23, '11:00 PM')])

    Email_Confirmation = BooleanField('Receive Email Confirmations for Meetings')
    submit = SubmitField('Save Changes')

class MeetingForm(FlaskForm):
    """Holds Meeting Forms for booking an appointments
                        
             Args:
                 Flaskform: imported from flask_wtf     
                        
            Attributes:
                 Title: Title for meeting textbox in webpage
                 Date: Date for Meeting textbox in webpage            
                 StartTime: Starting time for Meeting textbox in webpage       
                 Duration: Duration time for meeting textbox in webpage             
                 submit: Title for submit textbox in webpage 
                 
    """
    title = StringField('Meeting title',validators=[DataRequired])
    date=DateField('Choose date', format="%m/%d/%Y",validators=[DataRequired()])
    startTime=SelectField('Choose starting time(in 24hr expression)',coerce=int,choices=[(i,i) for i in range(9,19)])
    Duration = SelectField('Meeting Duration: ', choices=['15 minutes', '30 minutes', '1 hour'])
    submit = SubmitField('Submit Meeting')

    def validate_title(self,title):
        """ Validates if title is in database
        
            Args:
                 user: object in question for verification
            Returns:
                 If in use: Validation Error String  
                 
        """
    
        meeting=Meeting.query.filter_by(title=self.title.data).first()

        if meeting is not None: # username exist
            raise ValidationError('Please use another meeting title.')

    def validate_date(self,date):
        """ Validates if date is in database
        
            Args:
                 user: object in question for verification
            Returns:
                 If in use: Validation Error String  
                 
        """
    
        if self.date.data<datetime.datetime.now().date():
            raise ValidationError('You can only book for day after today.')   

class UserChoiceIterable(object):

    def __iter__(self):
        users = User.query.all()
        choices = [(user.id, f'{user.username}') for user in users] 
        for choice in choices:
            yield choice
                        
class DeleteForm(FlaskForm):
    ids = SelectField('Choose User', coerce=int, choices=UserChoiceIterable())
    submit = SubmitField('Delete')


