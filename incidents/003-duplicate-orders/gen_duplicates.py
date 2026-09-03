import csv
import random
from datetime import datetime, timedelta

random.seed(11)
day = datetime(2026, 8, 28)
normal_count = 150

with open('orders_aug28.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['order_id','customer_id','amount','currency','completed_at'])
    order_id = 300000
    originals = []
    for _ in range(normal_count):
        ts = day.replace(hour=random.randint(0,23), minute=random.randint(0,59), second=random.randint(0,59))
        cust = random.randint(1000,9999)
        amt = round(random.uniform(15,250),2)
        originals.append((cust, amt, ts))
        writer.writerow([order_id, cust, amt, 'USD', ts.strftime('%Y-%m-%d %H:%M:%S')])
        order_id += 1
    dupes = random.sample(originals, int(normal_count*0.15))
    for cust, amt, ts in dupes:
        dup_ts = ts + timedelta(seconds=random.randint(2,8))
        writer.writerow([order_id, cust, amt, 'USD', dup_ts.strftime('%Y-%m-%d %H:%M:%S')])
        order_id += 1
print("done")
