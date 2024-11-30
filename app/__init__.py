from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# Initialize SQLAlchemy without binding to the app yet
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.secret_key = 'my$ecretK3y!2024'

    # Configure the app
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'roomimages')

    # Enable debug mode
    app.debug = True  # This line enables debug mode

    # Initialize extensions
    db.init_app(app)

    # Register models and create database tables (for now, using db.create_all())
    from .models import Property
    with app.app_context():
        db.create_all()

    # Register blueprints or routes
    from .routes import main, admin  # Import both blueprints
    app.register_blueprint(main)
    app.register_blueprint(admin, url_prefix='/admin')  # Register admin blueprint with a prefix

    return app
