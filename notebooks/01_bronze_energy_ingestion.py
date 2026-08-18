# Databricks notebook source
# MAGIC %md
# MAGIC # Bronze Energy Meter Ingestion
# MAGIC Reads sample meter data with an explicit schema, adds audit metadata,
# MAGIC and writes the source-aligned dataset to Delta.

# COMMAND ----------

from src.bronze.bronze_ingestion import (
    add_ingestion_metadata,
    read_energy_meter_csv,
    write_bronze_delta,
)

# Update these paths for your Databricks workspace / Volume.
SOURCE_PATH = "/Volumes/energy_dev/raw/sample/energy_meter_readings.csv"
BRONZE_PATH = "/Volumes/energy_dev/bronze/energy_meter_readings"

# COMMAND ----------

raw_df = read_energy_meter_csv(spark, SOURCE_PATH)
bronze_df = add_ingestion_metadata(raw_df)

display(bronze_df)

# COMMAND ----------

write_bronze_delta(bronze_df, BRONZE_PATH)

# COMMAND ----------

print(f"Bronze ingestion completed. Rows processed: {bronze_df.count()}")
