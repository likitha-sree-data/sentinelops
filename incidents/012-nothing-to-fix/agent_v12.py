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

costs = bq_json("SELECT day, cost_usd, rows_processed FROM sentinelops_data.job_cost_012 ORDER BY day")
context = bq_json("SELECT * FROM sentinelops_data.business_context_012")

evidence = f"""
DAILY COST AND VOLUME, nightly_rollup JOB:
{json.dumps(costs, indent=2)}

BUSINESS CONTEXT:
{json.dumps(context, indent=2)}
"""

prompt = f"""Alert: cost for nightly_rollup has increased from $12.10 to $13.90 over the past week, a 15% rise.

Evidence:
{evidence}

Investigate this alert and give your assessment, with a confidence score (0 to 1) and reasoning tied to specific evidence above."""

client = genai.Client()
result = timed_generate(client, "gemini-3.6-flash", prompt)
print(result["text"])
print(f"\n[{result['elapsed_seconds']}s, {result['total_tokens']} tokens]")
