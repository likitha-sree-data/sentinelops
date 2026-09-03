import csv
import random
from datetime import datetime

random.seed(29)
day = datetime(2026, 8, 29)
rows = []
order_id = 500000

us_expected = 90
us_actual = int(us_expected * 0.75)
for _ in range(us_actual):
    ts = day.replace(hour=random.randint(0,23), minute=random.randint(0,59))
    amt = round(random.uniform(15,250),2)
    rows.append([order_id, 'US', amt, 'USD', ts.strftime('%Y-%m-%d %H:%M:%S')])
    order_id += 1

eu_count = 60
for _ in range(eu_count):
    ts = day.replace(hour=random.randint(0,23), minute=random.randint(0,59))
    amt = round(random.uniform(15,250),2)
    rows.append([order_id, 'EU', amt, 'EUR', ts.strftime('%Y-%m-%d %H:%M:%S')])
    order_id += 1

with open('regional_sales.csv','w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['order_id','region','amount','currency','completed_at'])
    writer.writerows(rows)
print(f"done, us={us_actual} (expected {us_expected}), eu={eu_count}")
