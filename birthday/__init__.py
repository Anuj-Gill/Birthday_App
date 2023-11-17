from flask import Flask

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os 
from dotenv import load_dotenv


app = Flask(__name__)
load_dotenv("../.env")
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY") #generated using secret module
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' #/// is for the relative paths, means that site.db will be created in the same file where py file is there
app.config["WTF_CSRF_ENABLED"] = False
db = SQLAlchemy(app) #instance of sqlalchemy
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from birthday import routes

app.app_context().push()