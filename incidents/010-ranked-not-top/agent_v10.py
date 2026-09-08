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

signups = bq_json("SELECT * FROM sentinelops_data.daily_signups_010 ORDER BY day")
campaign = bq_json("SELECT * FROM sentinelops_data.marketing_campaign_log_010")
channels = bq_json("SELECT * FROM sentinelops_data.signup_channel_summary_010 ORDER BY day, channel")
experiment = bq_json("SELECT * FROM sentinelops_data.experiment_assignments_010 ORDER BY variant")

evidence = f"""
DAILY SIGNUPS:
{json.dumps(signups, indent=2)}

MARKETING CAMPAIGN LOG:
{json.dumps(campaign, indent=2)}

SIGNUP CHANNEL BREAKDOWN (last 2 days):
{json.dumps(channels, indent=2)}

SIGNUP EXPERIMENT ASSIGNMENTS (2026-08-30):
{json.dumps(experiment, indent=2)}
"""

prompt = f"""Daily signups dropped from a steady ~200/day to 142 on 2026-08-30.

Evidence:
{evidence}

Investigate this drop. Give your top 3 ranked root causes with a confidence score (0 to 1) for each, and reasoning tied to specific evidence above. Do not treat correlation in timing alone as proof, check whether each candidate cause is actually consistent with all the evidence, not just the timing."""

client = genai.Client()
result = timed_generate(client, "gemini-3.6-flash", prompt)
print(result["text"])
print(f"\n[{result['elapsed_seconds']}s, {result['total_tokens']} tokens]")
