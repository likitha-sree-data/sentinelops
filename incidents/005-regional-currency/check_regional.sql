SELECT region, currency, COUNT(*) as orders, SUM(amount) as raw_amount_sum
FROM sentinelops_data.regional_sales
GROUP BY region, currency;
