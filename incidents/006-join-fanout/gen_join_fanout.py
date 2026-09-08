import csv
import random
from datetime import datetime

random.seed(6)
day = datetime(2026, 8, 30)
order_count = 150

with open('orders_aug30.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['order_id','customer_id','amount','currency','completed_at'])
    order_id = 600000
    order_ids = []
    for _ in range(order_count):
        ts = day.replace(hour=random.randint(0,23), minute=random.randint(0,59))
        amt = round(random.uniform(15,250),2)
        writer.writerow([order_id, random.randint(1000,9999), amt, 'USD', ts.strftime('%Y-%m-%d %H:%M:%S')])
        order_ids.append(order_id)
        order_id += 1

with open('order_promotions.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['order_id','promo_code'])
    duped_orders = random.sample(order_ids, int(order_count * 0.3))
    for oid in order_ids:
        writer.writerow([oid, 'SUMMER10'])
        if oid in duped_orders:
            writer.writerow([oid, 'LOYALTY5'])
print(f"done, {len(duped_orders)} orders have 2 promo rows instead of 1")
