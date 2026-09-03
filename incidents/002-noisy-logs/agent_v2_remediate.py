from google import genai

diagnosis_summary = """Top cause (confidence 0.95): orders_ingestion_job failed on 2026-08-26 and 2026-08-27 due to a network connectivity failure between the ingestion service and the upstream host api.ordersource.internal (connection refused errors), while the job succeeded normally on 2026-08-25 with no such errors."""

prompt = f"""Given this diagnosis:
{diagnosis_summary}

Propose ONE specific, safe remediation for this incident.

Include:
- confidence (0 to 1): how confident you are this action appropriately addresses the situation
- blast_radius: what is affected if this action turns out to be wrong or unnecessary
- reversibility: how this action could be undone if needed

Then describe exactly what should be implemented or done. If this is not something that can be fixed with a code, query, or view change, say so plainly instead of proposing one anyway.

Do not propose deleting or modifying any raw data."""

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
