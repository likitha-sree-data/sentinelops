import csv
import random
from datetime import datetime

random.seed(43)
incident_days = [datetime(2026,8,22), datetime(2026,8,23), datetime(2026,8,24)]
normal_daily = 150

# old format continuation, about 35% of normal volume, still using completed_at
with open('orders_raw_incident.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['order_id','customer_id','amount','currency','completed_at'])
    order_id = 100000
    for day in incident_days:
        count = int(normal_daily * 0.35) + random.randint(-5, 5)
        for _ in range(count):
            ts = day.replace(hour=random.randint(0,23), minute=random.randint(0,59))
            amount = round(random.uniform(15, 250), 2)
            writer.writerow([order_id, random.randint(1000,9999), amount, 'USD', ts.strftime('%Y-%m-%d %H:%M:%S')])
            order_id += 1

# new format, about 65% of normal volume, using the renamed column completed_ts
with open('orders_new_format.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['order_id','customer_id','amount','currency','completed_ts'])
    order_id = 200000
    for day in incident_days:
        count = int(normal_daily * 0.65) + random.randint(-5, 5)
        for _ in range(count):
            ts = day.replace(hour=random.randint(0,23), minute=random.randint(0,59))
            amount = round(random.uniform(15, 250), 2)
            writer.writerow([order_id, random.randint(1000,9999), amount, 'USD', ts.strftime('%Y-%m-%d %H:%M:%S')])
            order_id += 1
print("done")
