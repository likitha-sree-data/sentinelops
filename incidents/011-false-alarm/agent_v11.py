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

history = bq_json("SELECT day, active_users, EXTRACT(DAYOFWEEK FROM day) as day_of_week FROM sentinelops_data.daily_active_users_011 ORDER BY day")

evidence = f"""
DAILY ACTIVE USERS, LAST 28 DAYS (day_of_week: 1=Sunday, 7=Saturday):
{json.dumps(history, indent=2)}
"""

prompt = f"""Alert: daily active users on 2026-08-30 (758) fell below the 28-day average (approximately 960).

Evidence:
{evidence}

Investigate this alert. State your root cause finding, or state plainly if you believe this is not a genuine anomaly, with a confidence score (0 to 1) and reasoning tied to specific evidence above."""

client = genai.Client()
result = timed_generate(client, "gemini-3.6-flash", prompt)
print(result["text"])
print(f"\n[{result['elapsed_seconds']}s, {result['total_tokens']} tokens]")
