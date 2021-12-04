from flask import Flask
from config import Config
from flask_migrate import Migrate
# from .extensions import db, login_manager, toastr, ma
import logging
from logging.handlers import RotatingFileHandler
import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_toastr import Toastr
from flask_marshmallow import Marshmallow


app = Flask(__name__)
    # app = Flask(__name__, static_folder='./static/dist',
    #             template_folder='./static')

app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
toastr = Toastr(app)
login_manager = LoginManager(app)
ma = Marshmallow(app)

login_manager.login_view = 'auth.login'

if not app.debug:

    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/recipe.log', maxBytes=10240,
                                           backupCount=10)
    file_handler.setFormatter(logging.Formatter(
      '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Anime world')

# blueprint for auth routes in our app
from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

# blueprint for non-auth parts of app
from .main import main as main_blueprint
app.register_blueprint(main_blueprint)
