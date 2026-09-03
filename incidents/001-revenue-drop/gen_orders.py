import csv
import random
from datetime import datetime, timedelta

random.seed(42)
start_date = datetime(2026, 8, 1)
num_days = 21
orders_per_day = 150

with open('orders_seed.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['order_id', 'customer_id', 'amount', 'currency', 'completed_at'])
    order_id = 1
    for day_offset in range(num_days):
        day = start_date + timedelta(days=day_offset)
        for _ in range(orders_per_day + random.randint(-15, 15)):
            ts = day.replace(hour=random.randint(0,23), minute=random.randint(0,59))
            amount = round(random.uniform(15, 250), 2)
            writer.writerow([order_id, random.randint(1000, 9999), amount, 'USD', ts.strftime('%Y-%m-%d %H:%M:%S')])
            order_id += 1
print("done")
