CREATE OR REPLACE VIEW sentinelops_data.v_orders_deduplicated AS
WITH order_lags AS (
  SELECT order_id, customer_id, amount, currency, completed_at,
    TIMESTAMP_DIFF(completed_at, LAG(completed_at) OVER (
      PARTITION BY customer_id, CAST(amount AS NUMERIC), currency
      ORDER BY completed_at, order_id
    ), SECOND) AS seconds_since_prev
  FROM sentinelops_data.orders_raw
),
order_clusters AS (
  SELECT order_id, customer_id, amount, currency, completed_at,
    SUM(CASE WHEN seconds_since_prev IS NULL OR seconds_since_prev > 10 THEN 1 ELSE 0 END) OVER (
      PARTITION BY customer_id, CAST(amount AS NUMERIC), currency
      ORDER BY completed_at, order_id
    ) AS cluster_id
  FROM order_lags
)
SELECT order_id, customer_id, amount, currency, completed_at
FROM order_clusters
QUALIFY ROW_NUMBER() OVER (
  PARTITION BY customer_id, CAST(amount AS NUMERIC), currency, cluster_id
  ORDER BY completed_at, order_id
) = 1;
