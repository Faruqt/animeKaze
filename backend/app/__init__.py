import cloudinary
import logging
import os
from flask import Flask
from dotenv import load_dotenv

# extensions
from app.extensions import db, migrate, login_manager, marshmallow, mail, jwt

# config
from instance.config import app_config


# load environment variables fromm .env file
load_dotenv()


def create_app():
    app = Flask(__name__)

    config_name = os.environ.get("APP_SETTINGS", "development")

    app.config.from_object(
        app_config[config_name],
    )

    # set the logger level
    app.logger.setLevel(logging.INFO)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    mail.init_app(app)
    marshmallow.init_app(app)

    cloudinary.config(
        cloud_name=os.getenv("CLOUD_NAME"),
        api_key=os.getenv("API_KEY"),
        api_secret=os.getenv("API_SECRET"),
    )

    with app.app_context():
        # blueprint for app core

        # Import the views and blueprints after the app is created to avoid circular imports
        from app import views

        from app.api import api as api_blueprint
        from app.auth import auth as auth_blueprint

        app.register_blueprint(api_blueprint, url_prefix="/api")
        app.register_blueprint(auth_blueprint, url_prefix="/auth")

        return app
