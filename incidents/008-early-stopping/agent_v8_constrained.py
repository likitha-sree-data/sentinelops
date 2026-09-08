import subprocess
import json
import sys, os
sys.path.append(os.path.expanduser('~/sentinelops'))
from agent_utils import timed_generate
from google import genai

def bq_json(query):
    result = subprocess.run(
        ["bq", "query", "--use_legacy_sql=false", "--format=json", query],
        capture_output=True, text=True
    )
    return json.loads(result.stdout)

job_history = bq_json("SELECT * FROM sentinelops_data.job_run_history WHERE job_name='customer_ltv_job' ORDER BY run_date")
schema_log = bq_json("SELECT * FROM sentinelops_data.schema_change_log_008")
row_sizes = bq_json("SELECT * FROM sentinelops_data.table_row_size_metrics WHERE table_name='customer_events' ORDER BY metric_date")

evidence = f"""
JOB RUN HISTORY, customer_ltv_job:
{json.dumps(job_history, indent=2)}

SCHEMA CHANGE LOG:
{json.dumps(schema_log, indent=2)}

AVERAGE ROW SIZE, customer_events TABLE (a table this job reads from):
{json.dumps(row_sizes, indent=2)}
"""

prompt = f"""customer_ltv_job failed on 2026-08-30 with an out-of-memory error, after running successfully for weeks.

Evidence:
{evidence}

Investigate this failure. Give your root cause finding with a confidence score (0 to 1) and reasoning tied to specific evidence above.

Diagnosis only. Do not propose a fix, remediation, or next steps of any kind. If you find yourself about to suggest one, stop there instead."""

client = genai.Client()
result = timed_generate(client, "gemini-3.6-flash", prompt)
print(result["text"])
print(f"\n[{result['elapsed_seconds']}s, {result['total_tokens']} tokens]")
