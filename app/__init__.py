from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
 
app = Flask(__name__)
app.config.from_object(Config)

log_in = LoginManager(app)
log_in.login_view = 'login'

db = SQLAlchemy(app)
 
from app import routes, models 
