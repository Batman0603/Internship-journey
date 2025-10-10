import asyncio
import json
import os
from datetime import datetime

# Ensure the reports directory exists
REPORTS_DIR = "reports"
os.makedirs(REPORTS_DIR, exist_ok=True)

async def generate_report():
    """Simulates a long-running task and saves the result to a file."""
    print("[Analytics] Starting report generation...")
    await asyncio.sleep(5)  # Simulate heavy computation
    report_data = {"status": "Report generated successfully!", "generated_at": datetime.utcnow().isoformat()}
    file_path = os.path.join(REPORTS_DIR, "report.json")
    with open(file_path, "w") as f:
        json.dump(report_data, f)
    print(f"[Analytics] Report saved to {file_path}")
