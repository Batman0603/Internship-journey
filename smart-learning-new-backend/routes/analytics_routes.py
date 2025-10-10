from flask import Blueprint, jsonify, send_from_directory
import asyncio
import threading
import os
import json
from async_tasks.report_generator import generate_report

analytics_bp = Blueprint("analytics", __name__)

def run_async_task(task):
    """Helper to run an async task in a new thread with its own event loop."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(task)
    loop.close()

@analytics_bp.route("/generateReport", methods=["GET"])
def generate_report_route():
    """
    Starts a background job to generate a system report.
    This endpoint is protected by an API key.
    ---
    tags:
      - Analytics
    parameters:
      - in: query
        name: apiKey
        required: true
        type: string
        description: The secret API key for accessing analytics endpoints.
    responses:
      202:
        description: Report generation has started.
      403:
        description: Forbidden. Invalid API key.
    """
    # Run the long-running task in a background thread to avoid blocking.
    # The `generate_report` function now needs to handle its own logic, 
    # like saving the report to a file or database.
    thread = threading.Thread(target=run_async_task, args=(generate_report(),))
    thread.start()
    return jsonify({"message": "Report generation has started. It will be available shortly."}), 202

@analytics_bp.route("/getReport", methods=["GET"])
def get_report_route():
    """
    Retrieves the generated report if it is available.
    This endpoint is protected by an API key.
    ---
    tags:
      - Analytics
    parameters:
      - in: query
        name: apiKey
        required: true
        type: string
        description: The secret API key for accessing analytics endpoints.
    responses:
      200:
        description: The generated report data.
      202:
        description: Report is not yet available.
      403:
        description: Forbidden. Invalid API key.
    """
    """Serves the generated report file if it exists."""
    reports_dir = "reports"
    report_filename = "report.json"
    report_path = os.path.join(reports_dir, report_filename)

    if not os.path.exists(report_path):
        return jsonify({"status": "pending", "message": "Report is not yet available."}), 202

    with open(report_path, "r") as f:
        report_data = json.load(f)
    return jsonify(report_data), 200
