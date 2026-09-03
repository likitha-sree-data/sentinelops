DELETE FROM sentinelops_data.job_run_history
WHERE job_name IN ('us_region_feed','eu_region_feed') AND run_date = '2026-08-29';

INSERT INTO sentinelops_data.job_run_history (job_name, run_date, status, rows_processed, duration_seconds)
VALUES
('us_region_feed','2026-08-25','SUCCESS',91,10),
('us_region_feed','2026-08-26','SUCCESS',88,9),
('us_region_feed','2026-08-27','SUCCESS',93,10),
('us_region_feed','2026-08-28','SUCCESS',89,9),
('us_region_feed','2026-08-29','SUCCESS',67,9),
('eu_region_feed','2026-08-25','SUCCESS',59,11),
('eu_region_feed','2026-08-26','SUCCESS',61,10),
('eu_region_feed','2026-08-27','SUCCESS',58,11),
('eu_region_feed','2026-08-28','SUCCESS',62,10),
('eu_region_feed','2026-08-29','SUCCESS',60,11);
