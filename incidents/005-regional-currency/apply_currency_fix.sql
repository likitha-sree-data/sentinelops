CREATE OR REPLACE VIEW sentinelops_data.regional_revenue_rollup AS
SELECT 
    s.region, 
    DATE(s.completed_at) AS day, 
    COUNT(*) AS orders, 
    SUM(s.amount * COALESCE(c.usd_rate, 1.0)) AS revenue_usd
FROM sentinelops_data.regional_sales s
LEFT JOIN sentinelops_data.currency_rates c ON s.currency = c.currency
GROUP BY s.region, day;
