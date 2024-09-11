"""
views.py: This module contains the route handler for the root URL ("/").
"""

# library imports
from flask import current_app as app


@app.route("/", methods=["GET"])
def welcome():
    """
    Handle requests to the root URL ("/") by returning a welcome message.

    Returns:
        str: A welcome message.
    """
    return "Welcome to Anime Kaze!"
