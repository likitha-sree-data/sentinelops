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

all_job_history = bq_json("SELECT * FROM sentinelops_data.job_run_history WHERE job_name LIKE 'shipments_feed%' ORDER BY job_name, run_date")
registry = bq_json("SELECT * FROM sentinelops_data.pipeline_registry")

evidence = f"""
JOB RUN HISTORY, ALL JOBS MATCHING 'shipments_feed':
{json.dumps(all_job_history, indent=2)}

PIPELINE REGISTRY:
{json.dumps(registry, indent=2)}
"""

prompt = f"""Alert received: "shipments_feed job is failing, please investigate."

Evidence:
{evidence}

Investigate this alert. State clearly which job you believe the alert actually refers to, your confidence in that scoping decision, and your root cause finding."""

client = genai.Client()
result = timed_generate(client, "gemini-3.6-flash", prompt)
print(result["text"])
print(f"\n[{result['elapsed_seconds']}s, {result['total_tokens']} tokens]")
