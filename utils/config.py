import os

class Config:
    # MySQL Configuration
    MYSQL_USER = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "password")
    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_DB = os.getenv("MYSQL_DB", "smart_learning")

    # SQLAlchemy DB URI
    SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT Settings
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "supersecretkey")
    JWT_EXP_DELTA_SECONDS = 3600  # 1 hour
