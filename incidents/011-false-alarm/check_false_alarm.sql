SELECT day, active_users, EXTRACT(DAYOFWEEK FROM day) as day_of_week
FROM sentinelops_data.daily_active_users_011 ORDER BY day;
