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

with open('pipeline_query_definitions_006.txt') as f:
    view_definition = f.read()

real_summary = bq_json("SELECT COUNT(*) as order_count, SUM(amount) as revenue FROM sentinelops_data.orders_aug30")
view_summary = bq_json("SELECT COUNT(*) as row_count, SUM(amount) as revenue FROM sentinelops_data.daily_revenue_with_promos")
promo_check = bq_json("SELECT order_id, COUNT(*) as promo_rows FROM sentinelops_data.order_promotions GROUP BY order_id HAVING promo_rows > 1 LIMIT 10")

evidence = f"""
PRODUCTION VIEW DEFINITION:
{view_definition}

ORDERS TABLE SUMMARY (source of truth):
{json.dumps(real_summary, indent=2)}

VIEW OUTPUT SUMMARY (what's actually being reported):
{json.dumps(view_summary, indent=2)}

SAMPLE OF order_promotions ROWS WITH MORE THAN ONE ENTRY PER ORDER:
{json.dumps(promo_check, indent=2)}
"""

prompt = f"""You are investigating sentinelops_data.daily_revenue_with_promos for 2026-08-30. The reported order count and revenue look higher than expected.

Evidence:
{evidence}

Investigate and report your findings, with a confidence score (0 to 1) and reasoning tied to specific evidence above."""

client = genai.Client()
result = timed_generate(client, "gemini-3.6-flash", prompt)
print(result["text"])
print(f"\n[{result['elapsed_seconds']}s, {result['total_tokens']} tokens]")
