INSERT INTO sentinelops_data.job_run_history (job_name, run_date, status, rows_processed, duration_seconds)
VALUES
('shipments_feed','2026-08-13','SUCCESS',200,12),
('shipments_feed','2026-08-14','SUCCESS',198,11),
('shipments_feed','2026-08-15','SUCCESS',205,12),
('shipments_feed_v2','2026-08-27','SUCCESS',210,13),
('shipments_feed_v2','2026-08-28','SUCCESS',208,13),
('shipments_feed_v2','2026-08-29','SUCCESS',212,14),
('shipments_feed_v2','2026-08-30','SUCCESS',209,13),
('shipments_feed_v2','2026-08-31','FAILED',0,4);

CREATE TABLE sentinelops_data.pipeline_registry (
  job_name STRING, status STRING, notes STRING
);

INSERT INTO sentinelops_data.pipeline_registry (job_name, status, notes)
VALUES
('shipments_feed','deprecated','Replaced by shipments_feed_v2 on 2026-08-16. No longer scheduled.'),
('shipments_feed_v2','active','Current production shipments ingestion job, runs daily.');
