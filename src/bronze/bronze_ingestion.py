"""Bronze ingestion for the sample energy meter dataset.

The function keeps source values intact and adds ingestion metadata. In a
Databricks environment the same logic can write directly to a Delta table.
"""

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import current_timestamp, input_file_name, lit
from pyspark.sql.types import DoubleType, StringType, StructField, StructType, TimestampType  # noqa: I001


ENERGY_METER_SCHEMA = StructType(
    [
        StructField("meter_id", StringType(), False),
        StructField("reading_timestamp", TimestampType(), False),
        StructField("region", StringType(), False),
        StructField("energy_kwh", DoubleType(), False),
    ]
)


def read_energy_meter_csv(spark: SparkSession, source_path: str) -> DataFrame:
    """Read source CSV using an explicit schema."""
    return (
        spark.read.option("header", True)
        .schema(ENERGY_METER_SCHEMA)
        .csv(source_path)
    )


def add_ingestion_metadata(df: DataFrame, source_system: str = "energy_meter_csv") -> DataFrame:
    """Add audit columns without applying business transformations."""
    return (
        df.withColumn("source_system", lit(source_system))
        .withColumn("source_file", input_file_name())
        .withColumn("ingested_at", current_timestamp())
    )


def write_bronze_delta(df: DataFrame, target_path: str) -> None:
    """Persist the Bronze dataset as a Delta table."""
    (
        df.write.format("delta")
        .mode("append")
        .option("mergeSchema", "false")
        .save(target_path)
    )
