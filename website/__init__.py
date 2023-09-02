from flask import Flask #importing flask from flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager


# Creates a SQLAlchemy database instance
db = SQLAlchemy()
# Defines the database name
DB_NAME = "database.db"

# Function to create the Flask application
def create_app():
    app = Flask(__name__)
    # Set the Flask application's secret key
    app.config['SECRET_KEY'] = "imsobadatthis"
    # Set the SQLAlchemy database URI to use SQLite with the specified database name
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    # Initialize the database with the Flask app
    db.init_app(app)

    # Import views and auth blueprints
    from .views import views
    from .auth import auth

    # Register the blueprints with appropriate URL prefixes
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    # Import User, Note, Post, Comment, and Like models
    from .models import User, Note, Post, Comment, Like

    # Create the database tables within the application context
    with app.app_context():
        db.create_all()

    # Initialize the Flask-Login extension
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    # Define a function to load a user by their ID
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

# Function to create the database
def create_database(app):
    if not path.exists("website/" + DB_NAME):
        db.create_all(app=app)
        print("Created database!")
