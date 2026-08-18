-- Idempotent Silver upsert pattern.
-- The merge key represents the business grain of one meter reading.

MERGE INTO silver.energy_meter_readings AS target
USING silver_energy_updates AS source
ON target.meter_id = source.meter_id
AND target.reading_timestamp = source.reading_timestamp

WHEN MATCHED AND source.ingested_at > target.ingested_at THEN
  UPDATE SET *

WHEN NOT MATCHED THEN
  INSERT *;
