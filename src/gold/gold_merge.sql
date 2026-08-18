-- Production-style incremental Gold upsert pattern.
-- The fact table is atomic at meter_id + reading_timestamp grain.

MERGE INTO gold.fact_energy AS target
USING gold.fact_energy_updates AS source
ON target.meter_id = source.meter_id
AND target.reading_timestamp = source.reading_timestamp

WHEN MATCHED AND source.ingested_at > target.ingested_at THEN
  UPDATE SET *

WHEN NOT MATCHED THEN
  INSERT *;

-- Daily KPI upsert pattern. Reprocessing the same date/region replaces
-- the aggregate rather than creating duplicate KPI rows.
MERGE INTO gold.energy_daily_kpis AS target
USING gold.energy_daily_kpis_updates AS source
ON target.date_key = source.date_key
AND target.region = source.region

WHEN MATCHED THEN
  UPDATE SET *

WHEN NOT MATCHED THEN
  INSERT *;
