import os
from urllib.parse import quote_plus
import logging
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Attempt to load MySQL environment variables
    MYSQL_USER = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    MYSQL_DB = os.getenv("MYSQL_DB")
    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")

    # Check if MySQL variables are set. If not, fall back to a local SQLite database.
    if all([MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB]):
        if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
            logging.info("[DB] Using MySQL database configuration.")
        encoded_password = quote_plus(MYSQL_PASSWORD)
        # SQLAlchemy DB URI for MySQL
        SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{MYSQL_USER}:{encoded_password}@{MYSQL_HOST}/{MYSQL_DB}"
    else:
        logging.warning("="*60)
        logging.warning("[DB WARNING] MySQL environment variables not set.".center(60))
        logging.warning("Falling back to a temporary in-memory SQLite database.".center(60))
        logging.warning("Create a .env file with MySQL credentials for persistence.".center(60))
        logging.warning("="*60)
        SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
        
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT Settings
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "supersecretkey")
    JWT_EXP_DELTA_SECONDS = 3600  # 1 hour

    # Analytics API Key
    ANALYTICS_API_KEY = os.getenv("ANALYTICS_API_KEY")
