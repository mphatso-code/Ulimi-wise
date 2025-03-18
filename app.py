import os
import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_login import LoginManager
from translations import get_translation, get_available_languages


# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
# create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "ulimi_wise_default_secret")

# configure the database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///ulimi_wise.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# initialize the app with the extension
db.init_app(app)

# Setup flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Register Jinja filters
@app.template_filter('translate')
def translate_filter(text, lang='en'):
    """Filter to translate text in templates"""
    return get_translation(text, lang)

# Context processor to inject variables into all templates
@app.context_processor
def inject_globals():
    """Inject global variables into all templates"""
    from datetime import datetime
    now = datetime.now()
    return {
        'current_year': now.year,
        'current_time': now.strftime('%H:%M'),
        'get_available_languages': get_available_languages
    }

with app.app_context():
    # Make sure to import the models here or their tables won't be created
    import models  # noqa: F401
    db.create_all()

    # Import routes after db is initialized to avoid circular imports
    from routes import *

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))
