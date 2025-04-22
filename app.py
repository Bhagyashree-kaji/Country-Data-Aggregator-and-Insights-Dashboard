import os
import urllib.parse
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Set up logger
logger = logging.getLogger(__name__)

class Base(DeclarativeBase):
    pass

# Initialize SQLAlchemy with the Base class
db = SQLAlchemy(model_class=Base)

# Create the Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "country_data_aggregator_secret")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure the database with proper URL encoding for special characters
if os.environ.get("DATABASE_URL"):
    # Use environment variables directly for more control
    password = os.environ.get("PGPASSWORD", "")
    user = os.environ.get("PGUSER", "postgres")
    host = os.environ.get("PGHOST", "localhost")
    database = os.environ.get("PGDATABASE", "countrydata")
    port = os.environ.get("PGPORT", "5432")
    
    # Construct the URL with proper encoding for special characters
    db_url = f"postgresql://{user}:{urllib.parse.quote_plus(password)}@{host}:{port}/{database}"
    logger.info(f"Connecting to database at {host}:{port}/{database}")
else:
    # Fallback to SQLite for development if no DATABASE_URL
    db_url = "sqlite:///country_data.db"
    logger.info("Using SQLite database")

app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize the database with the app
db.init_app(app)

with app.app_context():
    # Import models here so tables are created
    import models  # noqa: F401
    
    # Import routes after models to avoid circular imports
    from routes.api import api_bp
    from routes.views import views_bp
    
    # Register blueprints
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(views_bp)
    
    # Create database tables
    db.create_all()
    logger.info("Database tables created")
