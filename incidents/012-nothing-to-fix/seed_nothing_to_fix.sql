CREATE TABLE sentinelops_data.job_cost_012 (day DATE, job_name STRING, cost_usd FLOAT64, rows_processed INT64);
INSERT INTO sentinelops_data.job_cost_012 (day, job_name, cost_usd, rows_processed) VALUES
('2026-08-24','nightly_rollup',12.10,510000),
('2026-08-25','nightly_rollup',12.40,522000),
('2026-08-26','nightly_rollup',12.30,518000),
('2026-08-27','nightly_rollup',12.60,530000),
('2026-08-28','nightly_rollup',13.10,548000),
('2026-08-29','nightly_rollup',13.40,560000),
('2026-08-30','nightly_rollup',13.90,580000);

CREATE TABLE sentinelops_data.business_context_012 (metric STRING, notes STRING);
INSERT INTO sentinelops_data.business_context_012 (metric, notes) VALUES
('month_end_volume','Order volume historically grows 10-15% in the last week of each month due to end-of-month customer purchasing patterns. This is expected and budgeted for.');
