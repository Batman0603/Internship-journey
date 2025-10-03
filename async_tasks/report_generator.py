import asyncio

async def generate_report():
    await asyncio.sleep(5)  # Simulate heavy computation
    return {"status": "Report generated successfully!"}
