"""Gold-layer dimensional model and analytics transformations.

The Gold layer exposes BI-ready fact and dimension datasets while keeping
business logic explicit, testable, and reusable.
"""

from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def build_dim_meter(silver_df: DataFrame) -> DataFrame:
    """Create a conformed meter dimension with a deterministic surrogate key."""
    return (
        silver_df.select("meter_id", "region")
        .dropDuplicates(["meter_id"])
        .withColumn("meter_key", F.xxhash64("meter_id"))
        .withColumn("effective_from", F.lit("2026-01-01").cast("date"))
        .withColumn("effective_to", F.lit("9999-12-31").cast("date"))
        .withColumn("is_current", F.lit(True))
    )


def build_dim_date(silver_df: DataFrame) -> DataFrame:
    """Create a date dimension covering the observed Silver date range."""
    bounds = silver_df.select(
        F.min(F.to_date("reading_timestamp")).alias("min_date"),
        F.max(F.to_date("reading_timestamp")).alias("max_date"),
    ).first()

    if bounds is None or bounds["min_date"] is None:
        return silver_df.sparkSession.createDataFrame([], "date_key date, year int, month int, day int, day_of_week int")

    return (
        silver_df.sparkSession.range(1)
        .select(F.explode(F.sequence(F.lit(bounds["min_date"]), F.lit(bounds["max_date"]))).alias("date_key"))
        .withColumn("year", F.year("date_key"))
        .withColumn("month", F.month("date_key"))
        .withColumn("day", F.dayofmonth("date_key"))
        .withColumn("day_of_week", F.dayofweek("date_key"))
    )


def build_fact_energy(silver_df: DataFrame, dim_meter: DataFrame) -> DataFrame:
    """Create the atomic energy fact at meter-reading grain."""
    meter_lookup = dim_meter.select("meter_id", "meter_key")

    return (
        silver_df.join(meter_lookup, on="meter_id", how="left")
        .withColumn("date_key", F.to_date("reading_timestamp"))
        .withColumn("reading_hour", F.hour("reading_timestamp"))
        .withColumn("reading_year", F.year("reading_timestamp"))
        .withColumn("reading_month", F.month("reading_timestamp"))
        .select(
            "meter_key",
            "date_key",
            "meter_id",
            "reading_timestamp",
            "reading_hour",
            "reading_year",
            "reading_month",
            "region",
            "energy_kwh",
            "source_system",
            "source_file",
            "ingested_at",
        )
    )


def build_energy_kpis(fact_energy: DataFrame) -> DataFrame:
    """Create daily regional KPIs for downstream BI consumption."""
    return (
        fact_energy.groupBy("date_key", "region")
        .agg(
            F.sum("energy_kwh").alias("total_energy_kwh"),
            F.avg("energy_kwh").alias("avg_meter_reading_kwh"),
            F.countDistinct("meter_id").alias("active_meter_count"),
            F.count("*").alias("reading_count"),
        )
        .withColumn("kwh_per_active_meter", F.col("total_energy_kwh") / F.col("active_meter_count"))
    )
