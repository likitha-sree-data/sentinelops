import subprocess
import json
import sys, os
sys.path.append(os.path.expanduser('~'))
from agent_utils import timed_generate
from google import genai

def bq_json(query):
    result = subprocess.run(
        ["bq", "query", "--use_legacy_sql=false", "--format=json", query],
        capture_output=True, text=True
    )
    return json.loads(result.stdout)

access_changes = bq_json("SELECT * FROM sentinelops_data.access_control_log ORDER BY changed_at")
query_summary = bq_json("SELECT principal, COUNT(*) as query_count, MIN(query_time) as first_query, MAX(query_time) as last_query FROM sentinelops_data.query_access_log GROUP BY principal ORDER BY first_query")
table_schema = bq_json("SELECT column_name, data_type FROM sentinelops_data.INFORMATION_SCHEMA.COLUMNS WHERE table_name='customer_pii'")

evidence = f"""
ACCESS CONTROL CHANGE LOG FOR TABLE customer_pii:
{json.dumps(access_changes, indent=2)}

QUERY ACCESS LOG, GROUPED BY PRINCIPAL:
{json.dumps(query_summary, indent=2)}

COLUMNS IN customer_pii:
{json.dumps(table_schema, indent=2)}
"""

prompt = f"""You are investigating an incident involving the table sentinelops_data.customer_pii.

Evidence:
{evidence}

Identify what happened, the root cause, and your assessment of the situation. Give a confidence score (0 to 1) for your root cause, and describe what you believe the impact and appropriate response should be."""

client = genai.Client()
result = timed_generate(client, "gemini-3.6-flash", prompt)
print(result["text"])
print(f"\n[{result['elapsed_seconds']}s, {result['total_tokens']} tokens]")
