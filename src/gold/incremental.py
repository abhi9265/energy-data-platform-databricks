"""Production-oriented incremental processing helpers for Gold Delta tables."""

from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def select_incremental_batch(df: DataFrame, watermark_column: str, last_watermark):
    """Return records strictly newer than the persisted watermark."""
    if last_watermark is None:
        return df
    return df.filter(F.col(watermark_column) > F.lit(last_watermark))


def affected_partitions(df: DataFrame) -> DataFrame:
    """Return distinct date/region keys requiring aggregate recomputation."""
    return df.select(
        F.to_date("reading_timestamp").alias("date_key"), "region"
    ).dropDuplicates()


def merge_fact_sql(catalog: str, schema: str) -> str:
    """Generate the idempotent atomic-fact MERGE contract."""
    return f"""
MERGE INTO {catalog}.{schema}.fact_energy AS target
USING fact_energy_updates AS source
ON target.meter_id = source.meter_id
AND target.reading_timestamp = source.reading_timestamp

WHEN MATCHED AND source.ingested_at > target.ingested_at THEN
  UPDATE SET *

WHEN NOT MATCHED THEN
  INSERT *
"""


def merge_daily_kpis_sql(catalog: str, schema: str) -> str:
    """Generate an affected-partition KPI replacement contract."""
    return f"""
MERGE INTO {catalog}.{schema}.energy_daily_kpis AS target
USING energy_daily_kpis_updates AS source
ON target.date_key = source.date_key
AND target.region = source.region

WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *
"""
