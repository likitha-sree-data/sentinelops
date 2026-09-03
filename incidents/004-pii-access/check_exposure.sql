SELECT principal, COUNT(*) as query_count, MIN(query_time) as first_query
FROM sentinelops_data.query_access_log
GROUP BY principal
ORDER BY first_query;
