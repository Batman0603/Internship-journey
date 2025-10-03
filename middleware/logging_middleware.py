import logging
from flask import request
from datetime import datetime
import os

# Define the log directory and ensure it exists before configuring logging
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Configure logging
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "flask.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_request_middleware(app):
    @app.before_request
    def log_request():
        logging.info(f"Request from {request.remote_addr}: {request.method} {request.path}")
