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

with open('pipeline_query_definitions.txt') as f:
    view_definition = f.read()

job_history = bq_json("SELECT * FROM sentinelops_data.job_run_history WHERE job_name IN ('us_region_feed','eu_region_feed') AND run_date BETWEEN '2026-08-25' AND '2026-08-29' ORDER BY job_name, run_date")
rates = bq_json("SELECT * FROM sentinelops_data.currency_rates")
regional_summary = bq_json("SELECT region, currency, COUNT(*) as orders, SUM(amount) as raw_amount_sum FROM sentinelops_data.regional_sales GROUP BY region, currency")

evidence = f"""
PRODUCTION VIEW DEFINITION:
{view_definition}

JOB RUN HISTORY FOR 2026-08-29:
{json.dumps(job_history, indent=2)}

CURRENCY RATES TABLE (available in the warehouse, for reference):
{json.dumps(rates, indent=2)}

REGIONAL SALES SUMMARY FOR 2026-08-29:
{json.dumps(regional_summary, indent=2)}
"""

prompt = f"""You are investigating sentinelops_data.regional_revenue_rollup for 2026-08-29. Something about the reported numbers for this day looks off compared to expectations.

Evidence:
{evidence}

Investigate and report your findings, with a confidence score (0 to 1) and reasoning tied to specific evidence above."""

client = genai.Client()
result = timed_generate(client, "gemini-3.6-flash", prompt)
print(result["text"])
print(f"\n[{result['elapsed_seconds']}s, {result['total_tokens']} tokens]")
