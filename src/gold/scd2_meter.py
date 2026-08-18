"""Transactional SCD Type 2 implementation for meter attributes."""

from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def prepare_meter_changes(current_dim: DataFrame, incoming: DataFrame) -> DataFrame:
    """Identify new or changed current meter versions."""
    current = current_dim.filter(F.col("is_current")).select(
        "meter_id", F.col("region").alias("current_region")
    )

    return (
        incoming.select("meter_id", "region")
        .dropDuplicates(["meter_id"])
        .join(current, "meter_id", "left")
        .filter(
            F.col("current_region").isNull()
            | ~F.col("region").eqNullSafe(F.col("current_region"))
        )
        .drop("current_region")
    )


def scd2_transaction_sql(catalog: str, schema: str) -> str:
    """Return the two-step Delta transaction contract for SCD2."""
    table = f"{catalog}.{schema}.dim_meter"
    return f"""
-- Step 1: expire changed current records.
MERGE INTO {table} AS target
USING meter_changes AS source
ON target.meter_id = source.meter_id
AND target.is_current = true
WHEN MATCHED AND NOT target.region <=> source.region THEN
  UPDATE SET
    target.effective_to = current_date() - INTERVAL 1 DAY,
    target.is_current = false;

-- Step 2: insert new current versions.
INSERT INTO {table}
  (meter_key, meter_id, region, effective_from, effective_to, is_current)
SELECT
  xxhash64(meter_id, current_date()),
  meter_id,
  region,
  current_date(),
  DATE '9999-12-31',
  true
FROM meter_changes;
"""
