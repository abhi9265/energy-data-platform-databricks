"""Incremental Gold merge and SCD2 helpers.

These helpers execute Delta Lake MERGE operations when a Databricks/Delta
runtime is available. The merge predicates are deterministic so replaying the
same source batch does not create duplicate fact or dimension rows.
"""

from delta.tables import DeltaTable
from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def upsert_fact_energy(source_df: DataFrame, target_path: str) -> None:
    """Upsert meter readings by their atomic meter/timestamp business key."""
    if DeltaTable.isDeltaTable(source_df.sparkSession, target_path):
        target = DeltaTable.forPath(source_df.sparkSession, target_path)
        (
            target.alias("target")
            .merge(
                source_df.alias("source"),
                "target.meter_id = source.meter_id "
                "AND target.reading_timestamp = source.reading_timestamp",
            )
            .whenMatchedUpdateAll(
                condition="source.ingested_at > target.ingested_at"
            )
            .whenNotMatchedInsertAll()
            .execute()
        )
    else:
        source_df.write.format("delta").mode("overwrite").save(target_path)


def upsert_daily_kpis(source_df: DataFrame, target_path: str) -> None:
    """Upsert daily regional aggregates idempotently."""
    if DeltaTable.isDeltaTable(source_df.sparkSession, target_path):
        target = DeltaTable.forPath(source_df.sparkSession, target_path)
        (
            target.alias("target")
            .merge(
                source_df.alias("source"),
                "target.date_key = source.date_key "
                "AND target.region = source.region",
            )
            .whenMatchedUpdateAll()
            .whenNotMatchedInsertAll()
            .execute()
        )
    else:
        source_df.write.format("delta").mode("overwrite").save(target_path)


def build_scd2_meter_updates(current_df: DataFrame, incoming_df: DataFrame) -> DataFrame:
    """Return incoming meter versions that differ from the current dimension."""
    incoming = incoming_df.select("meter_id", "region").dropDuplicates(["meter_id"])
    current = current_df.filter(F.col("is_current") == F.lit(True)).select(
        "meter_id", F.col("region").alias("current_region")
    )
    return (
        incoming.join(current, "meter_id", "left")
        .filter(F.col("current_region").isNull() | (F.col("region") != F.col("current_region")))
        .select("meter_id", "region")
        .withColumn("effective_from", F.current_date())
        .withColumn("effective_to", F.lit("9999-12-31").cast("date"))
        .withColumn("is_current", F.lit(True))
        .withColumn("meter_key", F.xxhash64("meter_id", "effective_from"))
    )
