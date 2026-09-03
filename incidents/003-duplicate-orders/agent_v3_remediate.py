import sys, os
sys.path.append(os.path.expanduser('~'))
from agent_utils import timed_generate
from google import genai

diagnosis_summary = """Top cause (confidence 0.95): Duplicate orders were created on 2026-08-28 because retried requests, triggered by timeouts, lacked an idempotency key, causing the same order to be inserted twice under different order_ids. 22 customer/amount pairs are affected."""

prompt = f"""Given this diagnosis:
{diagnosis_summary}

Propose ONE specific remediation.

Include:
- confidence (0 to 1)
- blast_radius: what is affected if this action is wrong
- reversibility: how this could be undone

Describe exactly what should be done, including any SQL if relevant."""

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
