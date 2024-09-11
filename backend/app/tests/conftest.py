"""
conftest.py: This module is used to define fixtures that can be used in multiple test modules.
"""

# library imports
import os
import pytest

from app.extensions import db
from instance.config import BASEDIR
from app import create_app


@pytest.fixture(scope="session", autouse=True)
def set_test_env():
    """
    Set environment variables for the test session.

    This fixture sets the environment variables required for the Flask application
    to run in a testing environment. It ensures that all tests run with the correct
    configuration settings.

    Note: This fixture is automatically applied to all tests due to autouse=True.
    """
    os.environ["APP_SETTINGS"] = "test"
    os.environ["FLASK_CONFIG"] = "test"
    os.environ["SECRET_KEY"] = "test_secret_key"


@pytest.fixture(scope="module")
def test_app():

    app = create_app()
    yield app


@pytest.fixture(scope="module")
def test_db(test_app):

    with test_app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()
