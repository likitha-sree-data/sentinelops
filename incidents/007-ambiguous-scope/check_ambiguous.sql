SELECT * FROM sentinelops_data.job_run_history WHERE job_name IN ('shipments_feed','shipments_feed_v2') ORDER BY job_name, run_date;
