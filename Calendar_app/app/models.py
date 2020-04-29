from app import db
from app import log_in
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    '''Database Tables
        
            Args:
                 db.Model: SQLALCHEMY class
                 
            Attributes:
                 id: Database counter
                 username: unique String of 64 characters
                 email: unique String of 128 characters
                 password_hash: String of 128 characters
    '''
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    
    def is_active(self):
        '''Returns True, if active user
         '''
        return (True)
    
    def is_authenticated(self):
        '''Returns True, if user is authenticated
        '''
        return (True)

    def is_anonymous(self):
        '''Returns False, if actual user
        '''
        return (False)

    def get_id(self):
        '''Returns id number for user_loader callback
        '''
        return str(self.id)
 
    def __repr__(self):
        '''Prints User object created in database
             Returns:
                 User {} "username object"             
        '''
        
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        '''Generates and sets hash for password_hash 
        '''
        self.password_hash = generate_password_hash(password)
 
    def check_password(self, password):
        '''Checks password_hash for given password
        '''
        return check_password_hash(self.password_hash, password)


class Meeting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(256))
    time = db.Column(db.DateTime, index=True)
    guest = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
 
    def __repr__(self):
        return '<Posts {}>'.format(self.body)

class Availability(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.Time, default='09:00:00')
    end = db.Column(db.Time, default='20:00:00')
    duration = db.Column(db.Time, default='00:30:00')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Start Time {}>'.format(self.start)


@log_in.user_loader
def load_user(id):
    '''Loads User 
    
            Args:
               id: int that identifies user          
            Properties: 
               reloads the user object from the user ID stored in session       
            Returns:
               User from id number               
    '''
    return User.query.get(int(id))
