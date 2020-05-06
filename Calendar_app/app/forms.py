from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TimeField, SelectField, DateField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError, NumberRange
from wtforms.fields.html5 import EmailField 
from wtforms.widgets import TextArea
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
    Duration = SelectField('Meeting Duration: ', choices=[('00:15:00', '15 minutes'), ('00:30:00', '30 minutes'), ('01:00:00', '1 hour')], validators=[DataRequired()])
    Start = SelectField('Availability Start Time', 
        choices= [('00:00:00', '12:00 AM'), ('01:00:00', '1:00 AM'), ('02:00:00', '2:00 AM'), ('03:00:00', '3:00 AM'), ('04:00:00', '4:00 AM'),
            ('05:00:00', '5:00 AM'), ('06:00:00', '6:00 AM'), ('07:00:00', '7:00 AM'), ('08:00:00', '8:00 AM'), ('09:00:00', '9:00 AM'),
            ('10:00:00', '10:00 AM'), ('11:00:00', '11:00 AM'), ('12:00:00', '12:00 PM'), ('13:00:00', '1:00 PM'), ('14:00:00', '2:00 PM'),
            ('15:00:00', '3:00 PM'), ('16:00:00', '4:00 PM'), ('17:00:00', '5:00 PM'), ('18:00:00', '6:00 PM'), ('19:00:00', '7:00 PM'),
            ('20:00:00', '8:00 PM'), ('21:00:00', '9:00 PM'), ('22:00:00', '10:00 PM'), ('23:00:00', '11:00 PM')])
    End = SelectField('Availability End Time', 
    choices= [('00:00:00', '12:00 AM'), ('01:00:00', '1:00 AM'), ('02:00:00', '2:00 AM'), ('03:00:00', '3:00 AM'), ('04:00:00', '4:00 AM'),
            ('05:00:00', '5:00 AM'), ('06:00:00', '6:00 AM'), ('07:00:00', '7:00 AM'), ('08:00:00', '8:00 AM'), ('09:00:00', '9:00 AM'),
            ('10:00:00', '10:00 AM'), ('11:00:00', '11:00 AM'), ('12:00:00', '12:00 PM'), ('13:00:00', '1:00 PM'), ('14:00:00', '2:00 PM'),
            ('15:00:00', '3:00 PM'), ('16:00:00', '4:00 PM'), ('17:00:00', '5:00 PM'), ('18:00:00', '6:00 PM'), ('19:00:00', '7:00 PM'),
            ('20:00:00', '8:00 PM'), ('21:00:00', '9:00 PM'), ('22:00:00', '10:00 PM'), ('23:00:00', '11:00 PM')], default='23:00:00')

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
    Guest = StringField("First and Last Name: ", validators=[DataRequired()])
    description = StringField('Meeting Description: ',validators=[DataRequired()], widget=TextArea())
    # date = DateField('Choose date', format="%m/%d/%Y",validators=[DataRequired()])     # date is chosen from calendar in profile
    startTime = SelectField('Choose starting time (in 24hr expression): ', coerce=str)
    # Duration = SelectField('Meeting Duration: ', choices=['15 minutes', '30 minutes', '1 hour'])      # allowed duration time is specified by creators 
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


