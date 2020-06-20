from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from app.src.config import Config

app = Flask(__name__)

# ALLOWED_CORS = "localhost"
# cors = CORS(app, resources={r"/*": {"origins": ALLOWED_CORS}})
cors = CORS(app)

# config
app.config.from_object(Config)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


from app import routes
