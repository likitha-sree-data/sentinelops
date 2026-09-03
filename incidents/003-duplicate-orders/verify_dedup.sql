SELECT COUNT(*) as total_rows FROM sentinelops_data.v_orders_deduplicated
WHERE DATE(completed_at) = "2026-08-28";

SELECT customer_id, amount, COUNT(*) as cnt
FROM sentinelops_data.v_orders_deduplicated
WHERE DATE(completed_at) = "2026-08-28"
GROUP BY customer_id, amount
HAVING cnt > 1;
