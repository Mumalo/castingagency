import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database

# TODO IMPLEMENT DATABASE URL
project_dir = os.path.dirname(os.path.abspath(__file__))
SQLALCHEMY_DATABASE_URI = 'postgresql://mac@localhost:5432/movies'
SECRET_KEY = 'kjdkjf4904i40jkejfkjdfdl'
SQLALCHEMY_TRACK_MODIFICATIONS = True