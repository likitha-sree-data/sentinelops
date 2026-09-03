import csv
import random
from datetime import datetime

random.seed(7)
days = [datetime(2026,8,25), datetime(2026,8,26), datetime(2026,8,27)]

with open('system_logs.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['log_time','log_level','service','message'])
    for day in days:
        for _ in range(80):
            ts = day.replace(hour=random.randint(0,23), minute=random.randint(0,59))
            writer.writerow([ts.strftime('%Y-%m-%d %H:%M:%S'), 'WARN', 'auth-service', 'token expired, refreshing'])
    for day in days[1:]:
        for _ in range(3):
            ts = day.replace(hour=random.randint(0,23), minute=random.randint(0,59))
            writer.writerow([ts.strftime('%Y-%m-%d %H:%M:%S'), 'ERROR', 'orders-ingestion', 'connection refused: upstream host api.ordersource.internal unreachable'])
print("done")
