CREATE OR REPLACE VIEW sentinelops_data.orders_deduplicated_test AS
WITH ranked_orders AS (
  SELECT order_id, customer_id, amount, currency, completed_at,
  ROW_NUMBER() OVER (PARTITION BY customer_id, CAST(amount AS NUMERIC), currency, completed_at ORDER BY order_id ASC) AS row_num
  FROM sentinelops_data.orders_raw
)
SELECT order_id, customer_id, amount, currency, completed_at
FROM ranked_orders WHERE row_num = 1;
