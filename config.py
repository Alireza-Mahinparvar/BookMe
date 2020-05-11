import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config():
    ''' Class that holds all the configuration setting for the project
    
        Attributes:
            SECRET_KEY: key used to prevent cross site attacks
            SQLALCHEMY_DATABASE_URI: location for database    
            SQLALCHEMY_TRACK_MODIFICATIONS: Modification tracker 
            
    '''
    SECRET_KEY = 'you-will-never-guess'

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
