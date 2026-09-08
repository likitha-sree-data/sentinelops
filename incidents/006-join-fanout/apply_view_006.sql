CREATE OR REPLACE VIEW sentinelops_data.daily_revenue_with_promos AS
SELECT o.order_id, o.amount, p.promo_code
FROM sentinelops_data.orders_aug30 o
JOIN sentinelops_data.order_promotions p ON o.order_id = p.order_id;
