INSERT INTO sentinelops_data.job_run_history (job_name, run_date, status, rows_processed, duration_seconds)
VALUES
('customer_ltv_job','2026-08-27','SUCCESS',500000,40),
('customer_ltv_job','2026-08-28','SUCCESS',498000,39),
('customer_ltv_job','2026-08-29','SUCCESS',501000,41),
('customer_ltv_job','2026-08-30','FAILED',0,55);

CREATE TABLE sentinelops_data.schema_change_log_008 (
  change_id INT64, table_name STRING, change_type STRING, changed_at TIMESTAMP, notes STRING
);
INSERT INTO sentinelops_data.schema_change_log_008 (change_id, table_name, change_type, changed_at, notes)
VALUES (1, 'customer_events', 'ADD COLUMN', TIMESTAMP('2026-08-29 00:00:00'),
'Added raw_payload STRING column to store full event payloads for debugging. Column added but not yet populated by upstream at time of migration.');

CREATE TABLE sentinelops_data.table_row_size_metrics (
  table_name STRING, metric_date DATE, avg_row_size_bytes INT64
);
INSERT INTO sentinelops_data.table_row_size_metrics (table_name, metric_date, avg_row_size_bytes)
VALUES
('customer_events','2026-08-27',850),
('customer_events','2026-08-28',860),
('customer_events','2026-08-29',870),
('customer_events','2026-08-30',48000);
