import subprocess
import json
from google import genai

def bq_json(query):
    result = subprocess.run(
        ["bq", "query", "--use_legacy_sql=false", "--format=json", query],
        capture_output=True, text=True
    )
    return json.loads(result.stdout)

rollup = bq_json("SELECT * FROM sentinelops_data.daily_revenue_rollup ORDER BY day")
migration_log = bq_json("SELECT * FROM sentinelops_data.schema_migration_log")
job_history = bq_json("SELECT * FROM sentinelops_data.job_run_history WHERE run_date >= '2026-08-18' ORDER BY run_date")
new_format_check = bq_json("SELECT COUNT(*) as new_format_orders FROM sentinelops_data.orders_new_format")

evidence = f"""
DAILY REVENUE ROLLUP:
{json.dumps(rollup, indent=2)}

SCHEMA MIGRATION LOG:
{json.dumps(migration_log, indent=2)}

RECENT JOB RUN HISTORY:
{json.dumps(job_history, indent=2)}

ORDERS SITTING IN A SEPARATE NEW-FORMAT TABLE (not included in the rollup above):
{json.dumps(new_format_check, indent=2)}
"""

prompt = f"""You are investigating a data incident. Daily revenue in the rollup below dropped sharply on the last 3 days, with no job failures reported anywhere.

Evidence:
{evidence}

Based only on this evidence, return the top 3 most likely root causes, ranked, each with:
- a confidence score from 0 to 1
- one sentence of reasoning tied to specific evidence above, not general speculation

Do not state a cause as fact unless the evidence directly supports it."""

client = genai.Client()
response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=prompt
)
print(response.text)
