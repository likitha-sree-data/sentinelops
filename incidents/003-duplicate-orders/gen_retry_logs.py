import csv
import random
from datetime import datetime

random.seed(12)
day = datetime(2026,8,28)

with open('retry_logs.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['log_time','log_level','service','message'])
    for _ in range(40):
        ts = day.replace(hour=random.randint(9,17), minute=random.randint(0,59))
        writer.writerow([ts.strftime('%Y-%m-%d %H:%M:%S'), 'WARN', 'orders-ingestion', 'request timeout after 5000ms, retrying without idempotency key'])
print("done")
