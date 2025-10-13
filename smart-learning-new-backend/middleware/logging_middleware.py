import logging
from flask import request
from datetime import datetime
import os

# Define the log directory and ensure it exists before configuring logging
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Get the root logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Create a formatter
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

# Create a file handler to write logs to a file
file_handler = logging.FileHandler(os.path.join(LOG_DIR, "flask.log"))
file_handler.setFormatter(formatter)

# Add both handlers to the root logger
logger.addHandler(file_handler)

def log_request_middleware(app):
    @app.before_request
    def log_request():
        logging.info(f"Request from {request.remote_addr}: {request.method} {request.path}")
