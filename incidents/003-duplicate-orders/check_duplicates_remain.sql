SELECT customer_id, amount, COUNT(*) as cnt
FROM sentinelops_data.orders_deduplicated_test
WHERE DATE(completed_at) = "2026-08-28"
GROUP BY customer_id, amount
HAVING cnt > 1;
