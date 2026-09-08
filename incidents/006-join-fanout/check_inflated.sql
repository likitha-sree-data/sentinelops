SELECT COUNT(*) as inflated_order_count, SUM(amount) as inflated_revenue
FROM sentinelops_data.daily_revenue_with_promos;
