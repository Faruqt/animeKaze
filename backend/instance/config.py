import os
from dotenv import load_dotenv
from datetime import timedelta

# load environment variables fromm .env file
load_dotenv()
BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(BASEDIR, "anime.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(BASEDIR, "anime/static/uploads")
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY") or "you-will-never-know"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        hours=int(os.environ.get("JWT_ACCESS_TOKEN_EXPIRES") or 1)
    )
    # CLOUD_NAME= os.environ.get('CLOUD_NAME')
    # API_KEY= os.environ.get('API_KEY')
    # API_SECRET=os.environ.get('API_SECRET')
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = int(os.environ.get("MAIL_PORT") or 25)
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS") is not None
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("SENDGRID_API_KEY")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER")
    ADMINS = os.environ.get("MAIL_ADMIN")


class ProductionConfig(Config):
    """
    Configuration settings for the production environment.
    """

    pass


class StagingConfig(Config):
    """
    Configuration settings for the staging environment.
    """

    pass


class DevelopmentConfig(Config):
    """
    Configuration settings for the development environment.
    """

    DEBUG = True


class TestConfig(Config):
    """
    Configuration settings for the testing environment.
    """

    TESTING = True
    DEBUG = True
    SERVER_NAME = "TESTSERVER.localdomain"
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


# Dictionary mapping configuration names to classes
app_config = {
    "test": TestConfig,
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "staging": StagingConfig,
}
