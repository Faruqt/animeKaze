"""
main.py: This module is used to initialize and run the Flask application.
"""

# local imports
from app import create_app  # import the create_app function from the app package


# create an instance of the Flask app using the create_app function
application = create_app()

# This is used to run the Flask application
# if the script is run directly from the command line
if __name__ == "__main__":
    application.run()
