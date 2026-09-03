import sys, os
sys.path.append(os.path.expanduser('~'))
from agent_utils import timed_generate
from google import genai

diagnosis_summary = """Top cause (confidence 0.95): Duplicate orders were created on 2026-08-28 because retried requests, triggered by timeouts, lacked an idempotency key, causing the same order to be inserted twice under different order_ids. 22 customer/amount pairs are affected."""

schema_context = """
Table sentinelops_data.orders_raw columns: order_id (INTEGER), customer_id (INTEGER), amount (FLOAT), currency (STRING), completed_at (TIMESTAMP). No status, cancel_reason, created_at, or updated_at columns exist. Do not invent any column not listed here.
"""

prompt = f"""Given this diagnosis:
{diagnosis_summary}

Schema, exact and complete:
{schema_context}

Propose the SAFEST possible remediation, one that does not alter, update, or delete any row in orders_raw. Prefer a downstream view or query that excludes duplicates for reporting purposes over any change to the raw table.

Include:
- confidence (0 to 1)
- blast_radius
- reversibility

Then give exact SQL valid against the schema above only."""

client = genai.Client()
result = timed_generate(client, "gemini-3.6-flash", prompt)
print(result["text"])
print(f"\n[{result['elapsed_seconds']}s, {result['total_tokens']} tokens]")
print("\n--- HUMAN APPROVAL REQUIRED ---")
approve = input("Approve this remediation? (y/n): ")
if approve.lower() == "y":
    print("Approved.")
else:
    print("Rejected. No changes made.")
