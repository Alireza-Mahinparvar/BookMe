from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError
from wtforms.fields.html5 import EmailField 
from .models import User

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
