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

job_history = bq_json("SELECT * FROM sentinelops_data.job_run_history WHERE run_date='2026-08-28'")
retry_logs = bq_json("SELECT log_time, log_level, service, message FROM sentinelops_data.system_logs WHERE service='orders-ingestion' AND DATE(log_time)='2026-08-28' LIMIT 10")
duplicate_pattern = bq_json("""SELECT customer_id, amount, COUNT(*) as cnt
FROM sentinelops_data.orders_raw
WHERE DATE(completed_at) = '2026-08-28'
GROUP BY customer_id, amount
HAVING cnt > 1
ORDER BY cnt DESC
LIMIT 10""")

evidence = f"""
JOB RUN HISTORY FOR 2026-08-28:
{json.dumps(job_history, indent=2)}

SAMPLE ORDERS-INGESTION SERVICE LOGS FOR 2026-08-28:
{json.dumps(retry_logs, indent=2)}

CUSTOMER/AMOUNT PAIRS APPEARING MORE THAN ONCE ON 2026-08-28 (sample):
{json.dumps(duplicate_pattern, indent=2)}
"""

prompt = f"""You are investigating a data incident. The orders_ingestion_job completed with SUCCESS status on 2026-08-28, but the order count and revenue for that day are noticeably higher than a typical day.

Evidence:
{evidence}

Identify the most likely root cause. Give your top cause with a confidence score (0 to 1) and reasoning tied to specific evidence above."""

client = genai.Client()
result = timed_generate(client, "gemini-3.6-flash", prompt)
print(result["text"])
print(f"\n[{result['elapsed_seconds']}s, {result['total_tokens']} tokens ({result['input_tokens']} in / {result['output_tokens']} out)]")
