from google import genai

diagnosis_summary = """Top cause (confidence 0.99): The daily_revenue_rollup view was not updated after the completed_at -> completed_ts schema migration on 2026-08-22, causing orders in orders_new_format to be silently excluded."""

schema_context = """
Table sentinelops_data.orders_raw columns: order_id (INTEGER), customer_id (INTEGER), amount (FLOAT), currency (STRING), completed_at (TIMESTAMP)
Table sentinelops_data.orders_new_format columns: order_id (INTEGER), customer_id (INTEGER), amount (FLOAT), currency (STRING), completed_ts (TIMESTAMP)
These are two separate tables with different column names for the same concept. Neither table contains both columns. Do not invent or assume any column not listed here.

The CURRENT view sentinelops_data.daily_revenue_rollup outputs exactly these columns and no others: day (DATE), orders (INTEGER, count of orders), revenue (FLOAT, sum of amount).
"""

prompt = f"""Given this diagnosis:
{diagnosis_summary}

Schema, exact and complete:
{schema_context}

Propose ONE specific, safe remediation. The fixed view MUST output exactly the same columns as the current view: day, orders, revenue. Do not rename, add, or remove any output column, and do not introduce new groupings like currency.

Include:
- confidence (0 to 1)
- blast_radius, explicitly stating whether the output schema changes at all
- reversibility

Then give exact SQL, valid against the schema above only.

Do not propose deleting or modifying any raw data. Only propose changes to views or queries."""

client = genai.Client()
response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=prompt
)
print(response.text)
print("\n--- HUMAN APPROVAL REQUIRED ---")
approve = input("Approve this remediation? (y/n): ")
if approve.lower() == "y":
    print("Approved.")
else:
    print("Rejected. No changes made.")
