from flask import Blueprint, jsonify
import asyncio
import threading
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
    # Run the long-running task in a background thread to avoid blocking.
    # The `generate_report` function now needs to handle its own logic, 
    # like saving the report to a file or database.
    thread = threading.Thread(target=run_async_task, args=(generate_report(),))
    thread.start()
    return jsonify({"message": "Report generation has started. It will be available shortly."}), 202
