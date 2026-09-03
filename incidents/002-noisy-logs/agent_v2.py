import subprocess
import json
from google import genai

def bq_json(query):
    result = subprocess.run(
        ["bq", "query", "--use_legacy_sql=false", "--format=json", query],
        capture_output=True, text=True
    )
    return json.loads(result.stdout)

job_history = bq_json("SELECT * FROM sentinelops_data.job_run_history WHERE job_name='orders_ingestion_job' ORDER BY run_date")
log_summary = bq_json("SELECT DATE(log_time) as day, log_level, service, message, COUNT(*) as cnt FROM sentinelops_data.system_logs GROUP BY day, log_level, service, message ORDER BY day, log_level")

evidence = f"""
JOB RUN HISTORY:
{json.dumps(job_history, indent=2)}

LOG SUMMARY (grouped by day, level, service, message):
{json.dumps(log_summary, indent=2)}
"""

prompt = f"""You are investigating a data pipeline incident. The orders_ingestion_job succeeded on 2026-08-25 but failed, processing 0 rows, on 2026-08-26 and 2026-08-27.

Evidence:
{evidence}

Identify the most likely root cause of the failures on Aug 26 and 27. Give your top cause with a confidence score (0 to 1) and reasoning tied to specific evidence above."""

client = genai.Client()
response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=prompt
)
print(response.text)
