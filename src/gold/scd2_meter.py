"""Slowly Changing Dimension Type 2 utilities for meter attributes."""

from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def prepare_meter_changes(current_dim: DataFrame, incoming: DataFrame) -> DataFrame:
    """Return incoming meter records that represent a new or changed version."""
    current = current_dim.filter(F.col("is_current") == True).select(
        "meter_id", F.col("region").alias("current_region")
    )

    return (
        incoming.select("meter_id", "region")
        .dropDuplicates(["meter_id"])
        .join(current, "meter_id", "left")
        .filter(
            F.col("current_region").isNull()
            | (F.col("region") != F.col("current_region"))
        )
        .drop("current_region")
    )


def scd2_merge_sql(catalog: str, schema: str) -> str:
    """Generate the Delta SQL contract used to apply SCD2 changes."""
    table = f"{catalog}.{schema}.dim_meter"
    return f"""
-- SCD Type 2 contract for {table}
-- 1. Expire the current version when a tracked attribute changes.
MERGE INTO {table} AS target
USING meter_changes AS source
ON target.meter_id = source.meter_id
AND target.is_current = true

WHEN MATCHED AND target.region <> source.region THEN
  UPDATE SET
    target.effective_to = current_date(),
    target.is_current = false;

-- 2. Insert the new current version in a follow-up MERGE/INSERT step.
INSERT INTO {table}
  (meter_key, meter_id, region, effective_from, effective_to, is_current)
SELECT
  xxhash64(meter_id, effective_from),
  meter_id,
  region,
  current_date(),
  DATE '9999-12-31',
  true
FROM meter_changes;
"""
