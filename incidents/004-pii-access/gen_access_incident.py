import csv
import random
from datetime import datetime, timedelta

random.seed(21)

with open('customer_pii.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['customer_id','email','phone','ssn_last4'])
    for i in range(100):
        writer.writerow([1000+i, f"customer{i}@example.com", f"555-01{i:02d}", f"{random.randint(1000,9999)}"])

with open('access_control_log.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['change_id','table_name','principal','access_level','changed_at','notes'])
    writer.writerow([1,'customer_pii','compliance_team','SELECT','2026-06-01 00:00:00','Original restricted access, set at table creation'])
    writer.writerow([2,'customer_pii','all_analysts','SELECT','2026-08-26 09:14:00','Broad IAM role update intended for a different, non-sensitive dataset accidentally included customer_pii in the affected resource group'])

with open('query_access_log.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['query_time','principal','table_name'])
    start = datetime(2026,8,12)
    for _ in range(30):
        ts = start + timedelta(days=random.randint(0,13), hours=random.randint(0,23))
        writer.writerow([ts.strftime('%Y-%m-%d %H:%M:%S'), 'compliance_team', 'customer_pii'])
    for _ in range(12):
        ts = datetime(2026,8,26) + timedelta(hours=random.randint(1,60))
        writer.writerow([ts.strftime('%Y-%m-%d %H:%M:%S'), f'analyst_{random.randint(1,8)}', 'customer_pii'])
print("done")
