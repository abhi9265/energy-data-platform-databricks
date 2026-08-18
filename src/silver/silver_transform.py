"""Production-style Silver transformation for energy meter data."""

from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql.window import Window

BUSINESS_KEYS = ["meter_id", "reading_timestamp"]


def standardize_source(df: DataFrame) -> DataFrame:
    """Normalize source attributes while retaining source lineage."""
    return (
        df.withColumn("meter_id", F.upper(F.trim("meter_id")))
        .withColumn("region", F.lower(F.trim("region")))
        .withColumn("reading_timestamp", F.to_timestamp("reading_timestamp"))
        .withColumn("energy_kwh", F.col("energy_kwh").cast("double"))
    )


def apply_data_quality_rules(df: DataFrame) -> DataFrame:
    """Assign deterministic quality status and reason codes."""
    invalid_conditions = (
        F.col("meter_id").isNull()
        | F.col("reading_timestamp").isNull()
        | F.col("region").isNull()
        | F.col("energy_kwh").isNull()
        | (F.col("energy_kwh") < 0)
    )

    return (
        df.withColumn(
            "dq_status",
            F.when(invalid_conditions, F.lit("REJECTED")).otherwise(F.lit("VALID")),
        )
        .withColumn(
            "dq_reason",
            F.when(F.col("meter_id").isNull(), "MISSING_METER_ID")
            .when(F.col("reading_timestamp").isNull(), "INVALID_TIMESTAMP")
            .when(F.col("region").isNull(), "MISSING_REGION")
            .when(F.col("energy_kwh").isNull(), "MISSING_ENERGY")
            .when(F.col("energy_kwh") < 0, "NEGATIVE_ENERGY")
            .otherwise(F.lit(None).cast("string")),
        )
    )


def deduplicate_valid_records(df: DataFrame) -> DataFrame:
    """Keep the latest ingestion for each business key."""
    window = Window.partitionBy(*BUSINESS_KEYS).orderBy(F.col("ingested_at").desc())
    return (
        df.filter(F.col("dq_status") == "VALID")
        .withColumn("record_rank", F.row_number().over(window))
        .filter(F.col("record_rank") == 1)
        .drop("record_rank")
    )


def build_silver(df: DataFrame) -> tuple[DataFrame, DataFrame]:
    """Return curated Silver records and a rejected-record quarantine set."""
    standardized = standardize_source(df)
    quality_checked = apply_data_quality_rules(standardized)
    rejected = quality_checked.filter(F.col("dq_status") == "REJECTED")
    curated = deduplicate_valid_records(quality_checked)
    return curated, rejected
