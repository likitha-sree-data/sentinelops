import sys, os
sys.path.append(os.path.expanduser('~'))
from agent_utils import timed_generate
from google import genai

diagnosis_summary = """Top cause (confidence 0.95): Duplicate orders were created on 2026-08-28 because retried requests, triggered by timeouts, lacked an idempotency key, causing the same order to be inserted twice under different order_ids, seconds apart, with the same customer_id and amount."""

schema_context = """
Table sentinelops_data.orders_raw columns: order_id (INTEGER), customer_id (INTEGER), amount (FLOAT64), currency (STRING), completed_at (TIMESTAMP). No status, cancel_reason, created_at, or updated_at columns exist.
Important: duplicate rows do NOT share the same completed_at value, they differ by 2 to 8 seconds. Grouping or partitioning by completed_at will fail to catch these duplicates.
Important: BigQuery does not allow FLOAT64 columns directly in a PARTITION BY clause inside OVER(). If amount is used in PARTITION BY, it must be written as CAST(amount AS NUMERIC), or the query will fail to run. GROUP BY allows FLOAT64 directly, this restriction is specific to PARTITION BY.
"""

prompt = f"""Given this diagnosis:
{diagnosis_summary}

Schema, exact and complete:
{schema_context}

Propose the SAFEST possible remediation, one that does not alter, update, or delete any row in orders_raw. Prefer a downstream view that excludes duplicates for reporting purposes.

Include:
- confidence (0 to 1)
- blast_radius
- reversibility

Then give exact SQL valid against the schema above only. Explain explicitly how your grouping logic still catches duplicates that occurred a few seconds apart."""

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
