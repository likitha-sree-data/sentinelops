SELECT day, cost_usd, rows_processed, ROUND(cost_usd / rows_processed * 1000000, 4) as cost_per_million_rows
FROM sentinelops_data.job_cost_012 ORDER BY day;
