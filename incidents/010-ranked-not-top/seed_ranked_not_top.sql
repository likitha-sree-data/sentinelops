CREATE TABLE sentinelops_data.daily_signups_010 (day DATE, signups INT64);
INSERT INTO sentinelops_data.daily_signups_010 (day, signups) VALUES
('2026-08-24',205),('2026-08-25',198),('2026-08-26',210),
('2026-08-27',202),('2026-08-28',195),('2026-08-29',207),('2026-08-30',142);

CREATE TABLE sentinelops_data.marketing_campaign_log_010 (campaign_name STRING, status STRING, changed_at TIMESTAMP, notes STRING);
INSERT INTO sentinelops_data.marketing_campaign_log_010 (campaign_name, status, changed_at, notes) VALUES
('spring_promo','PAUSED',TIMESTAMP('2026-08-29 18:00:00'),'Paused due to budget exhaustion for the month.');

CREATE TABLE sentinelops_data.signup_channel_summary_010 (day DATE, channel STRING, signups INT64);
INSERT INTO sentinelops_data.signup_channel_summary_010 (day, channel, signups) VALUES
('2026-08-29','paid',18),('2026-08-29','organic',189),
('2026-08-30','paid',16),('2026-08-30','organic',126);

CREATE TABLE sentinelops_data.experiment_assignments_010 (day DATE, variant STRING, users_assigned INT64, completed_signup INT64);
INSERT INTO sentinelops_data.experiment_assignments_010 (day, variant, users_assigned, completed_signup) VALUES
('2026-08-30','control_A',126,124),
('2026-08-30','signup_button_test_B',84,18);
